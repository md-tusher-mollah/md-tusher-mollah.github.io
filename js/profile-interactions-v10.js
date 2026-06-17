(function(){
  function firstLink(card){return card.querySelector('h3 a, .pub-title, a[href^="/publication/"]');}
  function hrefFrom(el){
    if(!el) return null;
    if(el.tagName && el.tagName.toLowerCase()==='a') return el.getAttribute('href');
    var a=el.closest && el.closest('a');
    return a ? a.getAttribute('href') : null;
  }
  document.querySelectorAll('.pub-card-compact,.pub-list-item,.pub-visual-card,.conference-card').forEach(function(card){
    var link=firstLink(card); var href=hrefFrom(link);
    if(!href) return;
    card.classList.add('card-clickable');
    card.setAttribute('tabindex','0');
    card.setAttribute('role','link');
    card.addEventListener('click',function(e){
      if(e.target.closest('a,button,input,textarea,select')) return;
      window.location.href=href;
    });
    card.addEventListener('keydown',function(e){
      if(e.key==='Enter' || e.key===' '){e.preventDefault(); window.location.href=href;}
    });
  });
})();
