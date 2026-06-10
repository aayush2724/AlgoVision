// frontend/js/vizScenes.js
// Real-world SVG visualizations for every problem type.
// Each scene is self-contained and draws into a provided container div.

export const VIZ_SCENES = {

  array: {
    label: "TRAIN CARRIAGES",
    color: "#5fd6e6",
    draw(container, problem) {
      const n = 8;
      const svg = makeSVG(500, 120);
      for (let i = 0; i < n; i++) {
        const x = 20 + i * 58;
        rect(svg, x, 30, 50, 60, "#0c2a31", "#5fd6e6");
        text(svg, x + 25, 65, (i + 1).toString(), "#a9f0fa", 14);
        // Connector
        if (i < n - 1) line(svg, x + 50, 60, x + 58, 60, "#2a7f8c", 2);
      }
      label(svg, 250, 110, problem.world, "#2a7f8c");
      container.appendChild(svg);
      animateStagger(svg.querySelectorAll('rect'), 'opacity', 0, 1, 60);
    }
  },

  tree: {
    label: "FAMILY TREE",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 260);
      const nodes = [
        {x:250,y:30}, {x:150,y:100},{x:350,y:100},
        {x:90,y:180},{x:200,y:180},{x:300,y:180},{x:420,y:180}
      ];
      const edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]];
      edges.forEach(([a,b]) => line(svg, nodes[a].x, nodes[a].y, nodes[b].x, nodes[b].y, "#0c2a31", 2));
      nodes.forEach((n,i) => {
        circle(svg, n.x, n.y, 22, "#0c2a31", "#5fd6e6");
        text(svg, n.x, n.y+5, `N${i+1}`, "#a9f0fa", 10);
      });
      label(svg, 250, 248, problem.world, "#2a7f8c");
      container.appendChild(svg);
      animateStagger(svg.querySelectorAll('circle'), 'r', 0, 22, 80);
    }
  },

  gps: {
    label: "GPS NAVIGATION",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 240);
      const nodes = [
        {x:80,y:60,l:"A"},{x:220,y:40,l:"B"},{x:160,y:140,l:"C"},
        {x:340,y:80,l:"D"},{x:300,y:180,l:"E"},{x:440,y:150,l:"F"}
      ];
      const edges = [[0,1,5],[0,2,3],[1,3,4],[2,3,6],[2,4,2],[3,5,3],[4,5,7]];
      edges.forEach(([a,b,w]) => {
        line(svg, nodes[a].x, nodes[a].y, nodes[b].x, nodes[b].y, "#0c2a31", 2);
        const mx = (nodes[a].x+nodes[b].x)/2, my = (nodes[a].y+nodes[b].y)/2;
        text(svg, mx, my-6, `${w}m`, "#2a7f8c", 9);
      });
      nodes.forEach(n => {
        circle(svg, n.x, n.y, 18, "#0c2a31", "#5fd6e6");
        text(svg, n.x, n.y+5, n.l, "#a9f0fa", 11);
      });
      // Animate a "path" highlight
      const pathNodes = [0,2,4,5];
      pathNodes.forEach((idx,i) => {
        setTimeout(() => {
          const c = svg.querySelectorAll('circle')[idx];
          c.setAttribute('fill', '#5fd6e6');
          c.setAttribute('filter', 'drop-shadow(0 0 6px #5fd6e6)');
        }, i * 400);
      });
      label(svg, 250, 228, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  social: {
    label: "SOCIAL NETWORK",
    color: "#a9f0fa",
    draw(container, problem) {
      const svg = makeSVG(500, 240);
      const nodes = [
        {x:250,y:40,l:"You"},{x:110,y:110,l:"A"},{x:390,y:110,l:"B"},
        {x:60,y:200,l:"C"},{x:175,y:200,l:"D"},{x:330,y:200,l:"E"},{x:450,y:200,l:"F"}
      ];
      [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]].forEach(([a,b]) =>
        line(svg, nodes[a].x, nodes[a].y, nodes[b].x, nodes[b].y, "#0c2a31", 2)
      );
      nodes.forEach((n,i) => {
        const col = i===0 ? "#5fd6e6" : "#0c2a31";
        circle(svg, n.x, n.y, i===0?24:18, col, "#2a7f8c");
        text(svg, n.x, n.y+5, n.l, "#dffafe", 9);
      });
      // Ripple BFS
      [[1,2],[3,4,5,6]].forEach((level, li) => {
        level.forEach(idx => setTimeout(() => {
          svg.querySelectorAll('circle')[idx].setAttribute('fill','rgba(95,214,230,0.3)');
        }, (li+1)*600));
      });
      label(svg, 250, 230, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  maze: {
    label: "MAZE EXPLORER",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 240);
      const CELL = 40, COLS = 10, ROWS = 5;
      for (let r = 0; r < ROWS; r++)
        for (let c = 0; c < COLS; c++) {
          const x = 25 + c*CELL, y = 20 + r*CELL;
          const isWall = (r===1&&c>=2&&c<=7)||(r===3&&c>=1&&c<=6);
          rect(svg, x, y, CELL-2, CELL-2, isWall ? "#06121a" : "#0c2a31",
               isWall ? "#06121a" : "#0c2a31");
        }
      circle(svg, 45, 40, 12, "#5fd6e6", "#a9f0fa");
      text(svg, 45, 44, "S", "#030a10", 10);
      circle(svg, 445, 200, 12, "#a9f0fa", "#5fd6e6");
      text(svg, 445, 204, "E", "#030a10", 10);
      label(svg, 250, 232, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  leaderboard: {
    label: "LEADERBOARD",
    color: "#a9f0fa",
    draw(container, problem) {
      const svg = makeSVG(500, 220);
      const vals = [4,7,2,9,1,6,3,8,5];
      vals.forEach((v,i) => {
        const h = v * 18, x = 20 + i*52, y = 180 - h;
        rect(svg, x, y, 44, h, "#0c2a31", i===3?"#a9f0fa":"#2a7f8c");
        text(svg, x+22, y-8, v.toString(), "#dffafe", 12);
      });
      label(svg, 250, 210, problem.world, "#2a7f8c");
      container.appendChild(svg);
      animateStagger(svg.querySelectorAll('rect'), 'height', 0, null, 80);
    }
  },

  stockchart: {
    label: "STOCK CHART",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 200);
      const prices = [42,38,55,48,65,72,58,80,74,88];
      const pts = prices.map((p,i) => `${30+i*46},${180-p*1.6}`).join(' ');
      const polyline = document.createElementNS("http://www.w3.org/2000/svg","polyline");
      polyline.setAttribute("points", pts);
      polyline.setAttribute("fill","none");
      polyline.setAttribute("stroke","#5fd6e6");
      polyline.setAttribute("stroke-width","2.5");
      svg.appendChild(polyline);
      prices.forEach((p,i) => circle(svg, 30+i*46, 180-p*1.6, 4, "#5fd6e6", "#5fd6e6"));
      label(svg, 250, 195, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  windowslide: {
    label: "SLIDING WINDOW",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 130);
      const arr = [3,1,4,1,5,9,2,6,5,3,5];
      arr.forEach((v,i) => {
        const x = 10+i*44, active = i>=2&&i<=5;
        rect(svg, x, 20, 40, 60, active?"rgba(95,214,230,0.15)":"#0c2a31",
             active?"#5fd6e6":"#2a7f8c");
        text(svg, x+20, 55, v.toString(), active?"#a9f0fa":"#2a7f8c", 14);
      });
      // Window bracket
      const bx = makeSVG_el("rect");
      bx.setAttribute("x","96"); bx.setAttribute("y","16");
      bx.setAttribute("width","180"); bx.setAttribute("height","68");
      bx.setAttribute("fill","none"); bx.setAttribute("stroke","#5fd6e6");
      bx.setAttribute("stroke-width","2");
      bx.setAttribute("stroke-dasharray","6,3");
      svg.appendChild(bx);
      label(svg, 250, 120, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  stack: {
    label: "PLATE STACK",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(200, 260);
      const vals = [3,7,1,9,4];
      vals.forEach((v,i) => {
        const y = 220 - i*44;
        rect(svg, 20, y, 160, 36, "#0c2a31", "#5fd6e6");
        text(svg, 100, y+22, `Item ${v}`, "#a9f0fa", 11);
      });
      text(svg, 100, 248, "← BOTTOM", "#2a7f8c", 9);
      text(svg, 100, 10, "TOP →", "#a9f0fa", 9);
      container.appendChild(svg);
    }
  },

  fractal: {
    label: "FRACTAL TREE",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 260);
      function branch(x1,y1,len,angle,depth) {
        if (depth===0) return;
        const x2 = x1+len*Math.sin(angle*(Math.PI/180));
        const x3 = x1+len*Math.sin(angle*(Math.PI/180)); // Fixed parameter shadowing
        const y2 = y1-len*Math.cos(angle*(Math.PI/180));
        const el = document.createElementNS("http://www.w3.org/2000/svg","line");
        el.setAttribute("x1",x1); el.setAttribute("y1",y1);
        el.setAttribute("x2",x2); el.setAttribute("y2",y2);
        el.setAttribute("stroke",`rgba(95,214,230,${0.15+depth*0.12})`);
        el.setAttribute("stroke-width", depth);
        svg.appendChild(el);
        branch(x2,y2,len*0.7,angle-25,depth-1);
        branch(x2,y2,len*0.7,angle+25,depth-1);
      }
      branch(250,250,60,0,7);
      label(svg, 250, 256, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  mirror: {
    label: "MIRROR / XOR",
    color: "#a9f0fa",
    draw(container, problem) {
      const svg = makeSVG(500, 200);
      // Two mirrored sequences
      const vals = [1,2,3,4,5,4,3,2,1];
      vals.forEach((v,i) => {
        const x = 15+i*52, mid = i===4;
        rect(svg, x, 60, 44, 80, mid?"rgba(95,214,230,0.2)":"#0c2a31",
             mid?"#a9f0fa":"#2a7f8c");
        text(svg, x+22, 105, v.toString(), mid?"#a9f0fa":"#dffafe", 14);
      });
      const midLine = makeSVG_el("line");
      midLine.setAttribute("x1","257"); midLine.setAttribute("y1","40");
      midLine.setAttribute("x2","257"); midLine.setAttribute("y2","170");
      midLine.setAttribute("stroke","#a9f0fa"); midLine.setAttribute("stroke-width","1");
      midLine.setAttribute("stroke-dasharray","4,4");
      svg.appendChild(midLine);
      label(svg, 250, 190, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  balance: {
    label: "BALANCE SCALE",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 220);
      // Fulcrum
      line(svg, 250, 60, 250, 120, "#2a7f8c", 3);
      line(svg, 100, 120, 400, 120, "#5fd6e6", 2);
      line(svg, 100, 120, 100, 170, "#2a7f8c", 2);
      line(svg, 400, 120, 400, 170, "#2a7f8c", 2);
      rect(svg, 50, 170, 100, 30, "#0c2a31", "#5fd6e6");
      rect(svg, 350, 170, 100, 30, "#0c2a31", "#2a7f8c");
      text(svg, 100, 190, "Left", "#a9f0fa", 10);
      text(svg, 400, 190, "Right", "#dffafe", 10);
      label(svg, 250, 215, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  timeline: {
    label: "TIMELINE / SCHEDULER",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 180);
      const jobs = [{s:1,e:4,l:"Job A"},{s:3,e:6,l:"Job B"},{s:5,e:8,l:"Job C"},{s:2,e:9,l:"Job D"}];
      const scale = 46;
      line(svg, 20, 30, 480, 30, "#2a7f8c", 1);
      for(let t=0;t<=10;t++) { line(svg,20+t*scale,25,20+t*scale,35,"#2a7f8c",1); text(svg,20+t*scale,22,t.toString(),"#2a7f8c",8); }
      jobs.forEach((j,i) => {
        const x=20+j.s*scale, w=(j.e-j.s)*scale;
        rect(svg, x, 50+i*30, w-2, 22, "#0c2a31", i%2===0?"#5fd6e6":"#a9f0fa");
        text(svg, x+w/2, 65+i*30, j.l, "#dffafe", 9);
      });
      label(svg, 250, 175, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  dna: {
    label: "DNA STRAND",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 180);
      const chars = "ATCGATCGATCG".split('');
      chars.forEach((c,i) => {
        const x=20+i*38, col=c==='A'?"#5fd6e6":c==='T'?"#a9f0fa":c==='C'?"#2a7f8c":"#dffafe";
        rect(svg, x, 60, 32, 60, "#0c2a31", col);
        text(svg, x+16, 95, c, col, 14);
        if(i<chars.length-1) line(svg,x+32,90,x+38,90,"#0c2a31",2);
      });
      label(svg, 250, 170, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  heap: {
    label: "HEAP / PRIORITY",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 240);
      const nodes = [{x:250,y:30,v:1},{x:150,y:100,v:3},{x:350,y:100,v:2},{x:90,y:180,v:7},{x:200,y:180,v:4},{x:300,y:180,v:5},{x:420,y:180,v:6}];
      [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]].forEach(([a,b])=>line(svg,nodes[a].x,nodes[a].y,nodes[b].x,nodes[b].y,"#0c2a31",2));
      nodes.forEach((n,i)=>{
        const col = i===0?"#5fd6e6":i<=2?"#2a7f8c":"#0c2a31";
        circle(svg,n.x,n.y,22,col,i===0?"#a9f0fa":"#5fd6e6");
        text(svg,n.x,n.y+5,n.v.toString(),"#dffafe",12);
      });
      label(svg, 250, 232, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  circuit: {
    label: "CIRCUIT / LOOP",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 200);
      // Circular chain of nodes
      const n=8, cx=250, cy=100, r=80;
      for(let i=0;i<n;i++){
        const a=(i/n)*Math.PI*2, b=((i+1)%n/n)*Math.PI*2;
        const x1=cx+r*Math.cos(a), y1=cy+r*Math.sin(a);
        const x2=cx+r*Math.cos(b), y2=cy+r*Math.sin(b);
        line(svg,x1,y1,x2,y2,"#5fd6e6",2);
        circle(svg,x1,y1,14,"#0c2a31","#2a7f8c");
        text(svg,x1,y1+4,(i+1).toString(),"#a9f0fa",10);
      }
      label(svg, 250, 192, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  grid: {
    label: "GRID / MATRIX",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 220);
      const CELL=44, ROWS=4, COLS=10;
      const data=[[1,0,1,1,0,1,0,1,1,0],[0,1,1,0,1,0,1,0,0,1],[1,1,0,1,0,1,1,0,1,0],[0,0,1,0,1,1,0,1,0,1]];
      for(let r=0;r<ROWS;r++) for(let c=0;c<COLS;c++){
        const v=data[r][c];
        rect(svg,10+c*CELL,10+r*CELL,CELL-2,CELL-2,v?"rgba(95,214,230,0.1)":"#06121a",v?"#5fd6e6":"#0c2a31");
        text(svg,10+c*CELL+CELL/2,10+r*CELL+CELL/2+5,v.toString(),v?"#a9f0fa":"#2a7f8c",12);
      }
      label(svg, 250, 212, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  mountain: {
    label: "MOUNTAIN PEAK",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 200);
      const pts = [0,20,40,80,110,145,170,140,100,60,30,10].map((v,i)=>`${20+i*42},${180-v}`).join(' ');
      const poly = document.createElementNS("http://www.w3.org/2000/svg","polyline");
      poly.setAttribute("points",pts);
      poly.setAttribute("fill","rgba(95,214,230,0.05)");
      poly.setAttribute("stroke","#5fd6e6");
      poly.setAttribute("stroke-width","2.5");
      svg.appendChild(poly);
      // Mark peak
      circle(svg, 20+6*42, 180-170, 8, "#a9f0fa", "#a9f0fa");
      label(svg, 250, 195, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  chess: {
    label: "CHESS BOARD",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(320, 320);
      for(let r=0;r<8;r++) for(let c=0;c<8;c++){
        rect(svg,c*38+10,r*38+10,36,36,(r+c)%2===0?"#0c2a31":"#06121a",(r+c)%2===0?"#2a7f8c":"#06121a");
      }
      // Queens placed
      [[0,1],[1,3],[2,5],[3,7],[4,2],[5,0],[6,6],[7,4]].forEach(([r,c])=>{
        text(svg,c*38+28,r*38+34,"♛","#a9f0fa",20);
      });
      container.appendChild(svg);
    }
  },

  canyon: {
    label: "CANYON / WATER",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 200);
      const heights = [0,1,0,2,1,0,1,3,2,1,2,1];
      const CELL=38;
      heights.forEach((h,i)=>{
        if(h>0) rect(svg,10+i*CELL,180-h*40,CELL-2,h*40,"#0c2a31","#2a7f8c");
      });
      // Water fill
      const waterLevel=2;
      heights.forEach((h,i)=>{
        const wh=Math.max(0,waterLevel-h)*40;
        if(wh>0) {
          const wr = makeSVG_el("rect");
          wr.setAttribute("x",10+i*CELL); wr.setAttribute("y",180-waterLevel*40);
          wr.setAttribute("width",CELL-2); wr.setAttribute("height",wh);
          wr.setAttribute("fill","rgba(95,214,230,0.25)");
          svg.appendChild(wr);
        }
      });
      label(svg, 250, 196, problem.world, "#2a7f8c");
      container.appendChild(svg);
    }
  },

  // ── Fast fallback for any unmapped viz type ──
  default: {
    label: "ALGORITHM",
    color: "#5fd6e6",
    draw(container, problem) {
      const svg = makeSVG(500, 160);
      text(svg, 250, 70, problem.world, "#5fd6e6", 16);
      text(svg, 250, 100, problem.hook, "#2a7f8c", 11);
      container.appendChild(svg);
    }
  }

};

// ── Shared SVG helpers ──────────────────────────────────────────────────────

function makeSVG(w, h) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
  svg.setAttribute("width", "100%");
  svg.setAttribute("style", "display:block; overflow:visible;");
  return svg;
}

function makeSVG_el(tag) {
  return document.createElementNS("http://www.w3.org/2000/svg", tag);
}

function rect(svg, x, y, w, h, fill, stroke) {
  const el = makeSVG_el("rect");
  el.setAttribute("x",x); el.setAttribute("y",y);
  el.setAttribute("width",w); el.setAttribute("height",h);
  el.setAttribute("fill",fill); el.setAttribute("stroke",stroke);
  el.setAttribute("stroke-width","1");
  svg.appendChild(el);
  return el;
}

function circle(svg, cx, cy, r, fill, stroke) {
  const el = makeSVG_el("circle");
  el.setAttribute("cx",cx); el.setAttribute("cy",cy); el.setAttribute("r",r);
  el.setAttribute("fill",fill); el.setAttribute("stroke",stroke);
  el.setAttribute("stroke-width","1.5");
  svg.appendChild(el);
  return el;
}

function line(svg, x1, y1, x2, y2, stroke, width) {
  const el = makeSVG_el("line");
  el.setAttribute("x1",x1); el.setAttribute("y1",y1);
  el.setAttribute("x2",x2); el.setAttribute("y2",y2);
  el.setAttribute("stroke",stroke); el.setAttribute("stroke-width",width);
  svg.appendChild(el);
  return el;
}

function text(svg, x, y, content, fill, size) {
  const el = makeSVG_el("text");
  el.setAttribute("x",x); el.setAttribute("y",y);
  el.setAttribute("text-anchor","middle");
  el.setAttribute("fill",fill); el.setAttribute("font-size",size);
  el.setAttribute("font-family","'VT323', monospace");
  el.textContent = content;
  svg.appendChild(el);
  return el;
}

function label(svg, x, y, content, fill) {
  const el = makeSVG_el("text");
  el.setAttribute("x",x); el.setAttribute("y",y);
  el.setAttribute("text-anchor","middle");
  el.setAttribute("fill",fill); el.setAttribute("font-size","10");
  el.setAttribute("font-family","'Press Start 2P', monospace");
  el.textContent = content.toUpperCase();
  svg.appendChild(el);
}

function animateStagger(els, prop, from, to, delayMs) {
  els.forEach((el, i) => {
    el.style.transition = `${prop} 0.4s ease ${i * delayMs}ms`;
    const original = to !== null ? to : el.getAttribute(prop);
    el.setAttribute(prop, from);
    setTimeout(() => el.setAttribute(prop, original), 50);
  });
}
