import {createServer} from "node:http";
import {readFile,stat} from "node:fs/promises";
import {resolve,extname,sep} from "node:path";
import {fileURLToPath} from "node:url";
const root=resolve(fileURLToPath(new URL(".",import.meta.url)));
const contentType={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",
 ".mjs":"text/javascript; charset=utf-8",".json":"application/json; charset=utf-8",
 ".png":"image/png",".css":"text/css; charset=utf-8",".wasm":"application/wasm"};
export const makeHandler=(rootDir=root)=>async (req,res)=>{
 try {
   const parsed=new URL(req.url,"http://127.0.0.1");
   if(req.method!=="GET" || !["/","/index.html","/main.js","/storyboard.mjs"].includes(parsed.pathname) && !parsed.pathname.startsWith("/node_modules/three/")){
      res.writeHead(404);res.end("Not found");return;
   }
   const base=resolve(rootDir);
   const target=resolve(base,"."+ (parsed.pathname==="/" ? "/index.html":parsed.pathname));
   if(!target.startsWith(base+sep)){res.writeHead(403);res.end();return}
   const st=await stat(target);
   if(!st.isFile() || st.size>16_000_000){res.writeHead(413);res.end();return}
   const content=await readFile(target);
   res.writeHead(200,{"Content-Type":contentType[extname(target)]||"application/octet-stream",
    "Cache-Control":"no-store","X-Content-Type-Options":"nosniff"});
   res.end(content);
 } catch(e){res.writeHead(404);res.end("Not found")}
};
if(process.argv[1] && fileURLToPath(import.meta.url)===resolve(process.argv[1])){
 const port=Number(process.env.KOSIF_THREE_PORT||45909);
 const server=createServer(makeHandler());
 server.listen(port,"127.0.0.1",()=>console.log(JSON.stringify({status:"ready",port,url:"http://127.0.0.1:"+port})));
}
