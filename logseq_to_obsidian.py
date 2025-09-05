import os,re,shutil,argparse,sys,yaml,unicodedata
from datetime import datetime
def slug(s): s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode("ascii"); s=re.sub(r"[\s_]+","-",s.strip()); s=re.sub(r"[^a-zA-Z0-9\/\-]","",s); s=re.sub(r"-+","-",s).strip("-"); return s.lower()
def parse_frontmatter(text):
    if text.startswith('---\n'):
        i=text.find('\n---\n',4)
        if i!=-1:
            y=text[4:i]; b=text[i+5:]
            try:
                return (yaml.safe_load(y) or {},b)
            except yaml.YAMLError:
                return ({},text)
    return ({},text)
def dump_frontmatter(meta): return '---\n'+yaml.safe_dump(meta,sort_keys=True,allow_unicode=True).strip()+"\n---\n"
def is_code_fence(line,flag):
    if re.match(r"^\s*```",line): return not flag
    return flag
def to_iso_date(s):
    s=s.strip()
    m=re.match(r"\[\[([0-9]{4})[_\-]([0-9]{2})[_\-]([0-9]{2})\]\]",s);
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m=re.match(r"([0-9]{4})[_\-]([0-9]{2})[_\-]([0-9]{2})",s)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    for fmt in ["%Y-%m-%d","%Y_%m_%d","%b %d, %Y","%B %d, %Y","%d %b %Y","%d %B %Y"]:
        try: return datetime.strptime(s,fmt).strftime("%Y-%m-%d")
        except: pass
    return None
def split_list_tags(v):
    parts=[]
    for x in re.split(r",|\s{2,}",v):
        x=x.strip()
        if not x: continue
        if x.startswith("[[") and x.endswith("]]"): x=x[2:-2]
        if x.startswith("#["): x=re.sub(r"^#\[\[|\]\]$","",x)
        if x.startswith("#"): x=x[1:]
        parts.append(slug(x))
    return [p for p in parts if p]
def md_path_title(root,fp):
    rel=os.path.relpath(fp,root)
    if rel.endswith(".md"): rel=rel[:-3]
    return rel.replace("\\","/")
def hyphen_date_name(name):
    m=re.match(r"^([0-9]{4})[_\-]([0-9]{2})[_\-]([0-9]{2})$",name);
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None
def convert_file(src_root,out_root,fp,opts,uuid_to_file,anchor_targets):
    with open(fp,"r",encoding="utf-8") as f: text=f.read()
    meta,body=parse_frontmatter(text)
    lines=body.splitlines()
    code=False
    # collect per-file tags from tags:: page-level properties at top
    page_tags=set()
    # pass 1: detect id:: for blocks, scheduled/deadline linkages, collect page properties
    last_block_idx=None; block_props={}
    for i,line in enumerate(lines):
        code=is_code_fence(line,code)
        if code: continue
        if re.match(r"^\s*$",line): continue
        if re.match(r"^\s*[-*]\s",line) or not line.startswith((" ","\t")): last_block_idx=i
        m=re.match(r"^\s*([A-Za-z0-9_\-]+)::\s*(.+?)\s*$",line)
        if m:
            k,v=m.group(1).lower(),m.group(2).strip()
            if k=="tags" and (last_block_idx is None or i<5):
                page_tags.update(split_list_tags(v));
            if k in ("id","scheduled","deadline","due","created","updated"):
                if last_block_idx is not None:
                    d=block_props.get(last_block_idx,{})
                    d[k]=v; block_props[last_block_idx]=d
    # insert ^uuid anchors
    for idx,props in block_props.items():
        if "id" in props:
            uid=re.sub(r"[^\w\-]","",props["id"])
            if uid:
                anchor_targets[uid]=(fp,idx)
                if "^"+uid not in lines[idx]: lines[idx]=lines[idx].rstrip()+" ^"+uid
    # convert tasks + scheduled/deadline to Tasks syntax and TODO/DONE → checkboxes
    def task_status(line):
        m=re.match(r"^(\s*[-*]\s+)(TODO|DOING|NOW|LATER|WAITING|CANCELED|CANCELLED|DONE)\s+(.*)$",line,flags=re.IGNORECASE)
        if not m: return None
        pre,kw,rest=m.groups(); kw=kw.upper()
        if kw in ("DONE","CANCELED","CANCELLED"): box="[x]"; tag="status/done" if opts.status_tags else None
        else: box="[ ]"; tag={"DOING":"status/doing","NOW":"status/now","LATER":"status/later","WAITING":"status/waiting","TODO":"status/todo"}.get(kw)
        if opts.status_tags and tag: rest=(rest+" #"+tag).rstrip()
        return pre+box+" "+rest
    for i in range(len(lines)):
        code=is_code_fence(lines[i],code)
        if code: continue
        ts=task_status(lines[i])
        if ts: lines[i]=ts
        if i in block_props:
            bp=block_props[i]
            for key,icon in (("scheduled","⏳"),("deadline","📅"),("due","📅")):
                if key in bp:
                    iso=to_iso_date(bp[key])
                    if iso and re.search(r"\[\s.\]",lines[i]):
                        if f"{icon} " not in lines[i]: lines[i]=lines[i].rstrip()+f" {icon} {iso}"
    # convert #[[Tag With Spaces]] → #tag-with-spaces ; [[YYYY_MM_DD]] → [[YYYY-MM-DD]]
    for i in range(len(lines)):
        code=is_code_fence(lines[i],code)
        if code: continue
        def repl_tag(m): return "#"+slug(m.group(1))
        lines[i]=re.sub(r"#\[\[([^\]]+)\]\]",repl_tag,lines[i])
        lines[i]=re.sub(r"\[\[([0-9]{4})_([0-9]{2})_([0-9]{2})\]\]",r"[[\1-\2-\3]]",lines[i])
    # rewrite ((uuid)) → [[path#^uuid]]
    def replace_block_refs(line):
        def repl(m):
            uid=m.group(1)
            if uid in uuid_to_file:
                tfile=uuid_to_file[uid]
                title=md_path_title(out_root or src_root,tfile)
                return f"[[{title}#^{uid}]]"
            return m.group(0)
        return re.sub(r"\(\(([a-f0-9\-]{6,})\)\)",repl,line,flags=re.IGNORECASE)
    for i in range(len(lines)):
        code=is_code_fence(lines[i],code)
        if code: continue
        lines[i]=replace_block_refs(lines[i])
    # page-level tags → YAML tags
    if opts.frontmatter:
        if page_tags:
            mtags=set([slug(t) for t in page_tags if t])
            old=set(meta.get("tags",[])) if isinstance(meta.get("tags"),list) else set()
            meta["tags"]=sorted(old.union(mtags))
        # file-level date for journals or existing created::
        base=os.path.splitext(os.path.basename(fp))[0]
        d=hyphen_date_name(base)
        if not d:
            for k in ("date","created","updated"):
                if k in meta and isinstance(meta[k],str) and to_iso_date(meta[k]): d=to_iso_date(meta[k]); break
        if not d and any(k in block_props.get(i,{}) for i in block_props for k in ("created","updated")):
            for i in block_props:
                for k in ("created","updated"):
                    if k in block_props[i]:
                        iso=to_iso_date(block_props[i][k])
                        if iso: d=iso; break
                if d: break
        if d: meta["date"]=d
    # optionally strip properties lines we converted
    if opts.strip_properties:
        new=[]
        code=False
        for i,line in enumerate(lines):
            code=is_code_fence(line,code)
            if code: new.append(line); continue
            m=re.match(r"^\s*([A-Za-z0-9_\-]+)::\s*(.+?)\s*$",line)
            if m and m.group(1).lower() in ("id","tags","scheduled","deadline","due","created","updated"):
                continue
            new.append(line)
        lines=new
    body="\n".join(lines).rstrip()+"\n"
    out_text=(dump_frontmatter(meta)+body) if opts.frontmatter and meta else (body if not text.startswith('---\n') else '---\n'+yaml.safe_dump(meta,sort_keys=True,allow_unicode=True).strip()+"\n---\n"+body)
    out_fp=fp
    if opts.out:
        out_fp=os.path.join(opts.out,os.path.relpath(fp,src_root)); os.makedirs(os.path.dirname(out_fp),exist_ok=True)
    if opts.dry_run: return {"out":out_fp,"changed":out_text!=text}
    with open(out_fp,"w",encoding="utf-8") as f: f.write(out_text)
    return {"out":out_fp,"changed":out_text!=text}
def build_uuid_index(src_root):
    idx={}
    for root,_,files in os.walk(src_root):
        for fn in files:
            if not fn.lower().endswith(".md"): continue
            fp=os.path.join(root,fn)
            try:
                with open(fp,"r",encoding="utf-8") as f: text=f.read()
            except: continue
            _,body=parse_frontmatter(text)
            for m in re.finditer(r"^\s*id::\s*([A-Za-z0-9\-\_]+)\s*$",body,flags=re.MULTILINE):
                uid=re.sub(r"[^\w\-]","",m.group(1))
                if uid and uid not in idx: idx[uid]=fp
    return idx
def maybe_copy_tree(src,out):
    if not out: return
    if os.path.abspath(src)==os.path.abspath(out): return
    if os.path.exists(out): 
        # If output exists, copy files from src to out
        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            out_dir = os.path.join(out, rel_path)
            os.makedirs(out_dir, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                out_file = os.path.join(out_dir, file)
                if not os.path.exists(out_file):
                    shutil.copy2(src_file, out_file)
    else: 
        shutil.copytree(src,out,dirs_exist_ok=True)
def rename_journals(out_root,opts):
    if not opts.rename_journals: return []
    renames=[]
    for root,_,files in os.walk(out_root):
        for fn in files:
            if not fn.lower().endswith(".md"): continue
            base=fn[:-3]; new=hyphen_date_name(base)
            if new and new!=base:
                src=os.path.join(root,fn); dst=os.path.join(root,new+".md")
                if opts.dry_run: renames.append((src,dst))
                else: os.rename(src,dst); renames.append((src,dst))
    return renames
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--src",required=True)
    p.add_argument("--out")
    p.add_argument("--dry-run",action="store_true")
    p.add_argument("--rename-journals",action="store_true")
    p.add_argument("--frontmatter",action="store_true")
    p.add_argument("--status-tags",action="store_true")
    p.add_argument("--strip-properties",action="store_true")
    args=p.parse_args()
    src=os.path.abspath(args.src); out=os.path.abspath(args.out) if args.out else None
    maybe_copy_tree(src,out)
    work_root=out or src
    uuid_to_file=build_uuid_index(work_root)
    anchor_targets={}
    changed=0; total=0
    for root,_,files in os.walk(work_root):
        for fn in files:
            if not fn.lower().endswith(".md"): continue
            fp=os.path.join(root,fn)
            res=convert_file(work_root,work_root,fp,args,uuid_to_file,anchor_targets)
            total+=1; changed+=1 if res["changed"] else 0
    renames=rename_journals(work_root,args)
    print(f"Processed {total} files; changed {changed}. Renamed {len(renames)} journals.")
    if args.dry_run:
        for s,d in renames: print(f"RENAME: {s} -> {d}")
if __name__=="__main__": main()
