(() => {
  "use strict";
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const $ = (id) => document.getElementById(id);
  const SIZE = 20, CELL = canvas.width / SIZE;
  const DIRS = { ArrowUp:{x:0,y:-1}, w:{x:0,y:-1}, ArrowDown:{x:0,y:1}, s:{x:0,y:1}, ArrowLeft:{x:-1,y:0}, a:{x:-1,y:0}, ArrowRight:{x:1,y:0}, d:{x:1,y:0} };
  const upgrades = [
    {id:"swift",name:"⚡ BƯỚC CHÂN NHANH",desc:"Tăng tốc độ di chuyển.",apply:g=>g.interval=Math.max(65,g.interval-12)},
    {id:"heart",name:"♥ SINH LỰC",desc:"Thêm một lần chịu va chạm.",apply:g=>g.lives++},
    {id:"magnet",name:"✧ TỪ TRƯỜNG",desc:"Nhận thêm 2 điểm mỗi tinh thể.",apply:g=>g.bonus+=2},
    {id:"guard",name:"⬡ GIÁP PHA LÊ",desc:"Bỏ qua lần va chạm tiếp theo.",apply:g=>g.shield++}
  ];
  let game, timer = null, lastTime = 0;
  const randomCell = () => ({x:Math.floor(Math.random()*SIZE),y:Math.floor(Math.random()*SIZE)});
  const same = (a,b) => a.x===b.x && a.y===b.y;
  function freeCell() {
    let p, tries=0;
    do { p=randomCell(); tries++; } while(tries<1000 && (game.snake.some(s=>same(s,p)) || game.walls.some(w=>same(w,p)) || (game.food&&same(game.food,p))));
    return p;
  }
  function newGame() {
    if(timer) clearInterval(timer);
    game={snake:[{x:9,y:10},{x:8,y:10},{x:7,y:10}],dir:{x:1,y:0},nextDir:{x:1,y:0},food:null,walls:[],score:0,best:Number(localStorage.getItem("nd-best")||0),lives:3,crystals:0,floor:1,bonus:0,shield:0,interval:155,paused:false,running:false,over:false,seed:Math.random().toString(36).slice(2,6).toUpperCase(),collected:0};
    addWalls(); game.food=freeCell(); updateUI(); draw();
    $("overlay-title").innerHTML="BƯỚC VÀO<br>HẦM NGỤC";
    $("overlay-text").textContent="Thu thập tinh thể. Tránh tường và bẫy. Mỗi tầng sẽ khó hơn.";
    $("start-btn").textContent="BẮT ĐẦU RUN ↗";
    $("overlay").classList.remove("hidden");
  }
  function addWalls() {
    game.walls=[];
    const count=Math.min(4+(game.floor-1)*3,25);
    for(let i=0;i<count;i++){const p=randomCell();if(!game.snake.some(s=>same(s,p))&&!game.walls.some(w=>same(w,p)))game.walls.push(p);}
  }
  function start() {
    if(game.over){newGame();}
    $("overlay").classList.add("hidden");game.running=true;game.paused=false;
    if(timer)clearInterval(timer);timer=setInterval(tick,game.interval);draw();
  }
  function tick() {
    if(!game.running||game.paused||game.over)return;
    game.dir=game.nextDir;
    const head={x:game.snake[0].x+game.dir.x,y:game.snake[0].y+game.dir.y};
    const wallHit=head.x<0||head.x>=SIZE||head.y<0||head.y>=SIZE||game.walls.some(w=>same(w,head));
    const eating=same(head,game.food);
    const body=game.snake.slice(0,eating?game.snake.length:game.snake.length-1).some(s=>same(s,head));
    if(wallHit||body){
      if(game.shield>0){game.shield--;game.nextDir={x:-game.dir.x,y:-game.dir.y};updateUI();draw();return;}
      game.lives--;updateUI();
      if(game.lives<=0){endGame();return;}
      game.snake=[{x:9,y:10},{x:8,y:10},{x:7,y:10}];game.dir={x:1,y:0};game.nextDir={x:1,y:0};game.walls=game.walls.filter(w=>!game.snake.some(s=>same(s,w)));draw();return;
    }
    game.snake.unshift(head);
    if(eating){
      game.score+=10+game.bonus;game.crystals++;game.collected++;
      game.food=freeCell();
      if(game.collected%3===0)showUpgrades();
      if(game.collected%5===0&&game.floor<10)nextFloor();
    }else game.snake.pop();
    if(game.score>game.best){game.best=game.score;localStorage.setItem("nd-best",String(game.best));}
    updateUI();draw();
  }
  function nextFloor(){
    game.floor++;game.score+=25;game.interval=Math.max(65,game.interval-8);
    if(timer){clearInterval(timer);timer=setInterval(tick,game.interval);}
    addWalls();game.food=freeCell();$("floor").textContent=String(game.floor).padStart(2,"0");
  }
  function showUpgrades(){
    game.paused=true;
    const box=$("upgrade-list");box.innerHTML="";
    const options=[...upgrades].sort(()=>Math.random()-.5).slice(0,3);
    options.forEach(u=>{
      const b=document.createElement("button");b.className="upgrade-btn";
      b.innerHTML="<strong>"+u.name+"</strong><span>"+u.desc+"</span>";
      b.addEventListener("click",()=>{u.apply(game);box.innerHTML='<div class="empty-upgrade">✧<br><span>Nâng cấp đã được áp dụng. Tiếp tục hành trình!</span></div>';game.paused=false;if(timer)clearInterval(timer);timer=setInterval(tick,game.interval);updateUI();draw();});
      box.appendChild(b);
    });
    $("overlay-title").innerHTML="CHỌN<br>NÂNG CẤP";
    $("overlay-text").textContent="Tinh thể cộng hưởng. Chọn một nâng cấp cho phần còn lại của run.";
    $("start-btn").textContent="TIẾP TỤC ↗";$("overlay").classList.remove("hidden");
    $("start-btn").onclick=()=>{$("overlay").classList.add("hidden");game.paused=false;if(timer)clearInterval(timer);timer=setInterval(tick,game.interval);};
  }
  function endGame(){
    game.over=true;game.running=false;if(timer)clearInterval(timer);
    $("overlay-title").innerHTML="RUN<br>KẾT THÚC";
    $("overlay-text").textContent="Bạn đạt "+game.score+" điểm tại tầng "+game.floor+". Hầm ngục đang chờ lượt tiếp theo.";
    $("start-btn").textContent="THỬ LẠI ↻";$("overlay").classList.remove("hidden");
    $("start-btn").onclick=()=>{newGame();start();};
    updateUI();draw();
  }
  function updateUI(){
    $("score").textContent=String(game.score).padStart(4,"0");$("best").textContent=String(game.best).padStart(4,"0");
    $("lives").textContent=Array.from({length:Math.min(game.lives,8)},()=>"♥").join(" ")||"—";
    $("crystals").textContent=game.crystals;$("floor").textContent=String(game.floor).padStart(2,"0");$("seed").textContent=game.seed;
    $("floor-goal").textContent=Math.min(game.floor,3)+" / 3";$("progress-bar").style.width=Math.min(100,game.floor/3*100)+"%";
  }
  function draw(){
    ctx.fillStyle="#0a1015";ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle="#17232a";ctx.lineWidth=1;
    for(let i=0;i<=SIZE;i++){ctx.beginPath();ctx.moveTo(i*CELL,0);ctx.lineTo(i*CELL,canvas.height);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*CELL);ctx.lineTo(canvas.width,i*CELL);ctx.stroke();}
    game.walls.forEach(w=>{ctx.fillStyle="#34424b";ctx.fillRect(w.x*CELL+3,w.y*CELL+3,CELL-6,CELL-6);ctx.strokeStyle="#53636d";ctx.strokeRect(w.x*CELL+5,w.y*CELL+5,CELL-10,CELL-10);});
    if(game.food){const cx=game.food.x*CELL+CELL/2,cy=game.food.y*CELL+CELL/2;ctx.save();ctx.shadowColor="#c7ff4f";ctx.shadowBlur=18;ctx.fillStyle="#c7ff4f";ctx.beginPath();ctx.moveTo(cx,cy-7);ctx.lineTo(cx+7,cy);ctx.lineTo(cx,cy+7);ctx.lineTo(cx-7,cy);ctx.closePath();ctx.fill();ctx.restore();}
    game.snake.forEach((s,i)=>{ctx.fillStyle=i===0?"#dfff94":i%2?"#9edb3d":"#b8f34d";ctx.shadowColor=i===0?"#c7ff4f":"transparent";ctx.shadowBlur=i===0?12:0;ctx.beginPath();ctx.roundRect(s.x*CELL+2,s.y*CELL+2,CELL-4,CELL-4,5);ctx.fill();ctx.shadowBlur=0;if(i===0){ctx.fillStyle="#17220d";const ex=s.x*CELL+CELL/2+(game.dir.x?game.dir.x*3:3),ey=s.y*CELL+CELL/2+(game.dir.y?game.dir.y*3:0);ctx.beginPath();ctx.arc(ex-game.dir.y*3,ey+game.dir.x*3,1.6,0,Math.PI*2);ctx.arc(ex+game.dir.y*3,ey-game.dir.x*3,1.6,0,Math.PI*2);ctx.fill();}});
    if(game.paused&&game.running){ctx.fillStyle="#0a101588";ctx.fillRect(0,0,canvas.width,canvas.height);}
  }
  document.addEventListener("keydown",e=>{
    const key=e.key.length===1?e.key.toLowerCase():e.key;
    if(DIRS[key]){e.preventDefault();const d=DIRS[key];if(d.x!==-game.dir.x||d.y!==-game.dir.y)game.nextDir=d;if(!game.running&&!game.over)start();}
    if(e.code==="Space"){e.preventDefault();if(game.running&&!game.over){game.paused=!game.paused;if(game.paused){$("overlay-title").textContent="TẠM DỪNG";$("overlay-text").textContent="Hầm ngục sẽ chờ bạn."; $("start-btn").textContent="TIẾP TỤC ↗";$("overlay").classList.remove("hidden");$("start-btn").onclick=()=>{$("overlay").classList.add("hidden");game.paused=false;};}else $("overlay").classList.add("hidden");}}
  });
  $("start-btn").addEventListener("click",start);$("restart-btn").addEventListener("click",()=>{newGame();start();});
  let touchStart=null;
  canvas.addEventListener("touchstart",e=>{touchStart={x:e.changedTouches[0].clientX,y:e.changedTouches[0].clientY};},{passive:true});
  canvas.addEventListener("touchend",e=>{if(!touchStart)return;const dx=e.changedTouches[0].clientX-touchStart.x,dy=e.changedTouches[0].clientY-touchStart.y;if(Math.max(Math.abs(dx),Math.abs(dy))>20){const d=Math.abs(dx)>Math.abs(dy)?{x:Math.sign(dx),y:0}:{x:0,y:Math.sign(dy)};if(d.x!==-game.dir.x||d.y!==-game.dir.y)game.nextDir=d;if(!game.running)start();}touchStart=null;},{passive:true});
  newGame();
})();