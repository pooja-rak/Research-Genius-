import streamlit as st
import json
from utils.api import call_claude, parse_json
from utils.db import save_result

def render():
    st.markdown("""<div style="font-family:'Pinyon Script',cursive;font-size:2.5rem;color:#FFD700;margin-bottom:0.2rem">Research Roadmap</div>
    <div style="font-size:0.8rem;color:#7a6030;margin-bottom:1.5rem">Knowledge graph · Force-directed layout · Interactive node exploration</div>""", unsafe_allow_html=True)

    with st.form("rm_form"):
        topic = st.text_input("Core Research Topic", placeholder="e.g. Deep learning for drug discovery and molecular property prediction")
        col1, col2 = st.columns(2)
        with col1:
            domain = st.selectbox("Domain", ["Biomedical", "Computer Science", "NLP / AI", "Climate Science", "Physics", "Social Sciences"])
        with col2:
            depth = st.selectbox("Graph Depth", ["Shallow (8 nodes)", "Medium (12 nodes)", "Deep (16 nodes)"])
        submitted = st.form_submit_button("✦ Generate Roadmap", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.warning("Please enter a topic."); return
        n = 8 if "Shallow" in depth else 12 if "Medium" in depth else 16

        sys = f"""You are a research knowledge graph engine. Respond ONLY in valid JSON — no markdown.

Schema:
{{
  "nodes": [
    {{"id":"n0","label":"<max 3 words>","type":"core","description":"<1 sentence>"}},
    ... more nodes with type: "subfield"|"bridge"|"gap"|"method"
  ],
  "links": [
    {{"source":"n0","target":"n1","strength":0.9,"relation":"<2-3 words>"}},
    ...
  ]
}}

Return exactly {n} nodes (1 core + rest split: 3-4 subfield, 2-3 bridge, 2-3 gap, 2-3 method).
Add {round(n*1.4)} links. strength 0.3-1.0. Make realistic for {domain} domain."""

        with st.spinner("Building your knowledge graph..."):
            raw = call_claude(sys, f"Topic: \"{topic}\"\nDomain: {domain}\nNodes: {n}")
        if not raw: return
        d = parse_json(raw)
        if not d: return

        nodes = d.get("nodes", [])
        links = d.get("links", [])

        color_map = {"core":"#FFD700","subfield":"#5DCAA5","bridge":"#AFA9EC","gap":"#F0997B","method":"#888780"}

        # Build interactive D3 graph as HTML component
        nodes_json = json.dumps(nodes)
        links_json = json.dumps(links)
        color_json = json.dumps(color_map)

        html = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
body{{margin:0;background:#1a1208;font-family:'Nunito',sans-serif;overflow:hidden}}
#graph{{width:100%;height:480px}}
.tooltip{{position:absolute;background:rgba(26,18,8,0.95);border:1px solid rgba(255,215,0,0.3);border-radius:9px;padding:10px 14px;font-size:12px;color:#fff8d6;pointer-events:none;max-width:200px;line-height:1.5;z-index:10;display:none}}
.legend{{position:absolute;bottom:12px;left:12px;display:flex;flex-wrap:wrap;gap:8px}}
.leg-item{{display:flex;align-items:center;gap:5px;font-size:10px;color:#7a6030}}
.leg-dot{{width:9px;height:9px;border-radius:50%}}
</style>
</head>
<body>
<svg id="graph"></svg>
<div class="tooltip" id="tt"></div>
<div class="legend">
<div class="leg-item"><div class="leg-dot" style="background:#FFD700"></div>Your topic</div>
<div class="leg-item"><div class="leg-dot" style="background:#5DCAA5"></div>Subfield</div>
<div class="leg-item"><div class="leg-dot" style="background:#AFA9EC"></div>Bridge</div>
<div class="leg-item"><div class="leg-dot" style="background:#F0997B"></div>Gap</div>
<div class="leg-item"><div class="leg-dot" style="background:#888780"></div>Method</div>
</div>
<script>
const nodes={nodes_json};
const links={links_json};
const COLORS={color_json};
const W=document.getElementById('graph').clientWidth||700, H=480;
const svg=d3.select('#graph').attr('width',W).attr('height',H);
const g=svg.append('g');
svg.call(d3.zoom().scaleExtent([0.3,4]).on('zoom',e=>g.attr('transform',e.transform)));
const sim=d3.forceSimulation(nodes)
  .force('link',d3.forceLink(links).id(d=>d.id).distance(d=>100-d.strength*30).strength(0.6))
  .force('charge',d3.forceManyBody().strength(-250))
  .force('center',d3.forceCenter(W/2,H/2))
  .force('collision',d3.forceCollide(32));
const link=g.selectAll('line').data(links).enter().append('line')
  .attr('stroke',d=>COLORS[nodes.find(n=>n.id===(d.source?.id||d.source))?.type]||'#888')
  .attr('stroke-opacity',0.4).attr('stroke-width',d=>d.strength*2.2);
const node=g.selectAll('.ng').data(nodes).enter().append('g').attr('class','ng').style('cursor','pointer')
  .call(d3.drag().on('start',(e,d)=>{{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}})
    .on('drag',(e,d)=>{{d.fx=e.x;d.fy=e.y;}}).on('end',(e,d)=>{{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}))
  .on('mousemove',(e,d)=>{{
    const tt=document.getElementById('tt');
    tt.style.display='block';tt.style.left=(e.offsetX+14)+'px';tt.style.top=(e.offsetY-10)+'px';
    tt.innerHTML='<strong style="color:'+COLORS[d.type]+'">'+d.label+'</strong><br><span style="font-size:10px;opacity:.7;text-transform:uppercase">'+d.type+'</span><br>'+d.description;
  }}).on('mouseleave',()=>document.getElementById('tt').style.display='none');
node.append('circle').attr('r',d=>d.type==='core'?20:12).attr('fill',d=>COLORS[d.type]||'#888')
  .attr('fill-opacity',d=>d.type==='core'?1:0.75).attr('stroke',d=>d.type==='core'?'#fff':'rgba(255,255,255,0.25)').attr('stroke-width',1.5);
node.append('text').attr('text-anchor','middle').attr('dy','3em').attr('font-size',d=>d.type==='core'?'11px':'10px')
  .attr('font-weight','700').attr('fill',d=>d.type==='core'?'#FFD700':'rgba(255,251,230,0.85)')
  .attr('font-family','Nunito,sans-serif').text(d=>d.label.length>16?d.label.slice(0,14)+'…':d.label);
sim.on('tick',()=>{{
  link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
  node.attr('transform',d=>`translate(${{Math.max(24,Math.min(W-24,d.x))}},${{Math.max(24,Math.min(H-24,d.y))}})`);}});
</script>
</body></html>"""

        st.components.v1.html(html, height=500)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Node Details**")
        cols = st.columns(4)
        type_labels = {"core":"🎯 Core","subfield":"🔬 Subfield","bridge":"🌉 Bridge","gap":"💡 Gap","method":"🔧 Method"}
        for i, node in enumerate(nodes):
            with cols[i % 4]:
                color = color_map.get(node.get("type",""), "#888")
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid {color}33;border-radius:9px;padding:0.7rem;margin-bottom:0.5rem">
                <div style="font-size:0.65rem;font-weight:800;color:{color};text-transform:uppercase;letter-spacing:1px">{type_labels.get(node.get('type',''),'')}</div>
                <div style="font-size:0.8rem;font-weight:700;color:#fffbe6;margin:0.2rem 0">{node.get('label','')}</div>
                <div style="font-size:0.7rem;color:#7a6030;line-height:1.4">{node.get('description','')[:90]}</div>
                </div>""", unsafe_allow_html=True)

        save_result("roadmap", topic, d, 80)
        st.success("✓ Saved to tracker")
