/* Fold POS site chrome: shops dropdown, mobile menu, hairline on scroll. */
(function(){
  var nav=document.querySelector('.fx-nav'); if(!nav) return;
  var drop=nav.querySelector('.fx-drop-btn'), panel=document.getElementById('fx-shops');
  var burger=nav.querySelector('.fx-burger'), menu=document.getElementById('fx-menu');
  function setDrop(open){ if(!drop) return; drop.setAttribute('aria-expanded',open?'true':'false'); panel.classList.toggle('open',open); }
  if(drop){
    drop.addEventListener('click',function(e){ e.stopPropagation(); setDrop(drop.getAttribute('aria-expanded')!=='true'); });
    document.addEventListener('click',function(e){ if(!panel.contains(e.target)) setDrop(false); });
    drop.parentNode.addEventListener('focusout',function(e){ if(!drop.parentNode.contains(e.relatedTarget)) setDrop(false); });
  }
  function setMenu(open){
    burger.setAttribute('aria-expanded',open?'true':'false'); menu.classList.toggle('open',open);
    document.body.classList.toggle('fx-locked',open);
    if(open) menu.style.setProperty('--fx-top',nav.getBoundingClientRect().bottom+'px');
    nav.classList.toggle('fx-solid',open);
  }
  if(burger&&menu){
    burger.addEventListener('click',function(){ setMenu(burger.getAttribute('aria-expanded')!=='true'); });
    menu.addEventListener('click',function(e){ if(e.target.closest('a')) setMenu(false); });
  }
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'){ setDrop(false); if(menu&&menu.classList.contains('open')){ setMenu(false); burger.focus(); } } });
  window.addEventListener('scroll',function(){ nav.classList.toggle('scrolled',window.scrollY>8); },{passive:true});
  window.addEventListener('resize',function(){ if(window.innerWidth>1040&&menu&&menu.classList.contains('open')) setMenu(false); });
})();

(function(){
  // One 22-second story, driven by a single clock:
  // the van pulls up, the worker comes out with an empty cart, loads the linens from the van,
  // turns and wheels them into the shop while the van drives off.
  var svg=document.querySelector('.fx-scene svg'); if(!svg) return;
  var $=function(id){return svg.getElementById?svg.getElementById(id):document.getElementById(id)};
  var T=22, S=1.3, VY=293.7, VSTOP=820, VIN=1660, VOUT=-40;
  var W=$('fsW'), body=$('fsBody'), L1=$('fsL1'), L1p=$('fsL1p'), L2=$('fsL2'), L2p=$('fsL2p'),
      CW1=$('fsCW1'), CW2=$('fsCW2'), van=$('fsVan'), vtext=$('fsVanText'), vdoor=$('fsVDoor'),
      VW1=$('fsVW1'), VW2=$('fsVW2'), door=$('fsDoor'), items=[$('fsI1'),$('fsI2'),$('fsI3'),$('fsI4')];
  var ITEM_AT=[11.0,11.7,12.4,13.1], ITEM_C=[[46,-57],[68,-54],[86,-47],[72,-76]];
  var PX_OUT=1185, PX_LOAD=939, PX_IN=1125, SPEED=54;
  var WALK1=[6.3, 6.3+(PX_OUT-PX_LOAD)/SPEED], TURN=[13.8,14.5], WALK2=[15.3, 15.3+(PX_IN-PX_LOAD)/SPEED];
  var c=function(x){return x<0?0:x>1?1:x}, seg=function(t,a,b){return c((t-a)/(b-a))};
  var eo=function(x){return 1-Math.pow(1-x,3)}, ei=function(x){return x*x*x}, eio=function(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
  function vanX(t){
    if(t<5) return VIN+(VSTOP-VIN)*eo(t/5);
    if(t<15.2) return VSTOP;
    return VSTOP+(VOUT-VSTOP)*ei(seg(t,15.2,19.7));
  }
  function doorS(t){ // 1 closed, .16 open
    var o=Math.max(Math.min(seg(t,5.9,6.3),1-seg(t,8.6,9.0)), Math.min(seg(t,14.9,15.3),1-seg(t,19.3,19.7)));
    return 1-.84*eio(o);
  }
  function worker(t){
    var px, f=-1, dist=0, moving=0;
    if(t<WALK1[1]){ var u=seg(t,WALK1[0],WALK1[1]); px=PX_OUT+(PX_LOAD-PX_OUT)*u; dist=(PX_OUT-px); moving=Math.min(seg(t,WALK1[0],WALK1[0]+.25),1-seg(t,WALK1[1]-.25,WALK1[1])); }
    else if(t<WALK2[0]){ px=PX_LOAD; dist=PX_OUT-PX_LOAD; }
    else { var u2=seg(t,WALK2[0],WALK2[1]); px=PX_LOAD+(PX_IN-PX_LOAD)*u2; dist=(PX_OUT-PX_LOAD)+(px-PX_LOAD); moving=Math.min(seg(t,WALK2[0],WALK2[0]+.25),1-seg(t,WALK2[1]-.25,WALK2[1])); }
    if(t>=TURN[0]) f=-1+2*eio(seg(t,TURN[0],TURN[1]));
    return {px:px,f:f,dist:dist,moving:moving};
  }
  function legs(phi,amp){
    [[L2,L2p,0],[L1,L1p,Math.PI]].forEach(function(l){
      var p=phi+l[2], a=19*Math.cos(p)*amp, k=Math.max(0,Math.sin(p))*amp;
      l[0].setAttribute('transform','rotate('+a.toFixed(2)+' 14 -32)');
      l[1].setAttribute('d','M14 -32 L'+(14+5*k).toFixed(2)+' '+(-17-k).toFixed(2)+' L'+(14-2*k).toFixed(2)+' '+(-3-3*k).toFixed(2)+' h6');
    });
  }
  function render(t){
    t=((t%T)+T)%T;
    // van
    var vx=vanX(t), bounce=t>5&&t<5.6?1.3*Math.sin(Math.PI*(t-5)/.6)*(1-(t-5)/.6):0;
    van.setAttribute('transform','translate('+vx.toFixed(2)+' '+(VY+bounce).toFixed(2)+') scale('+(-S)+' '+S+')');
    vtext.setAttribute('transform','translate('+(vx-55*S).toFixed(2)+' '+(VY+bounce).toFixed(2)+') scale('+S+')');
    var vdist=t<15.2?(VIN-vx):(VIN-VSTOP)+(VSTOP-vx), vdeg=vdist/(11*S)*57.2958;
    VW1.setAttribute('transform','translate(32 60) rotate('+vdeg.toFixed(1)+')');
    VW2.setAttribute('transform','translate(126 60) rotate('+vdeg.toFixed(1)+')');
    var dopen=Math.min(eio(seg(t,5.4,5.9)),1-eio(seg(t,14.0,14.5)));
    vdoor.setAttribute('transform','scale('+dopen.toFixed(3)+' 1)');
    // shop door
    var ds=doorS(t); door.setAttribute('transform','translate(1165 0) scale('+ds.toFixed(3)+' 1) translate(-1165 0)');
    // worker
    var w=worker(t), vis=t>6.2&&t<19.2;
    W.setAttribute('opacity',vis?1:0);
    W.setAttribute('transform','translate('+w.px.toFixed(2)+' 341) scale('+w.f.toFixed(3)+' 1) translate(-15 0)');
    var phi=w.dist/46*2*Math.PI; legs(phi,w.moving);
    body.setAttribute('transform','translate(0 '+(-1.6*Math.abs(Math.sin(phi))*w.moving).toFixed(2)+')');
    var cdeg=(w.dist/5.2*57.2958).toFixed(1);
    CW1.setAttribute('transform','translate(40 -5) rotate('+cdeg+')'); CW2.setAttribute('transform','translate(86 -5) rotate('+cdeg+')');
    // linens: each one is handed out of the van and lands in the cart
    var sx=15+PX_LOAD-826, sy=322-341;
    items.forEach(function(it,i){
      var a=ITEM_AT[i], u=seg(t,a,a+.55);
      if(t<a){ it.setAttribute('opacity',0); return; }
      it.setAttribute('opacity',1);
      if(u>=1){ var land=t<a+.8?-1.5*Math.sin(Math.PI*(t-a-.55)/.25):0; it.setAttribute('transform','translate(0 '+land.toFixed(2)+')'); return; }
      var e=eio(u), dx=(sx-ITEM_C[i][0])*(1-e), dy=(sy-ITEM_C[i][1])*(1-e)-30*Math.sin(Math.PI*u), r=(1-e)*-25;
      it.setAttribute('transform','translate('+dx.toFixed(2)+' '+dy.toFixed(2)+') rotate('+r.toFixed(1)+' '+ITEM_C[i][0]+' '+ITEM_C[i][1]+')');
    });
  }
  window.fsRender=function(t){ render(t); if(svg.setCurrentTime){ svg.pauseAnimations(); svg.setCurrentTime(t); } };
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){ window.fsRender(14.7); return; }
  var clock=0, last=null, running=false, raf=0, frozen=false;
  function tick(now){ if(last!==null) clock+=Math.min(.1,(now-last)/1000); last=now; render(clock); raf=requestAnimationFrame(tick); }
  function start(){ if(running||frozen) return; running=true; last=null; if(svg.unpauseAnimations) svg.unpauseAnimations(); raf=requestAnimationFrame(tick); }
  function stop(){ if(!running) return; running=false; cancelAnimationFrame(raf); if(svg.pauseAnimations) svg.pauseAnimations(); }
  render(0); stop(); if(svg.pauseAnimations) svg.pauseAnimations();
  if('IntersectionObserver' in window){ new IntersectionObserver(function(es){ es.forEach(function(e){ e.isIntersecting?start():stop(); }); }).observe(svg); } else start();
  window.fsStop=function(){ frozen=true; stop(); };
})();
