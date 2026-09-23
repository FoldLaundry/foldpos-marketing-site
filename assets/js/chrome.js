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
