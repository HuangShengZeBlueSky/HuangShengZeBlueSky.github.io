function activate(buttons,button,panels,matches){
 buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 panels.forEach(p=>p.hidden=!matches(p));
}
document.querySelectorAll('[data-secant]').forEach(root=>{
 const slider=root.querySelector('[data-secant-slider]'),line=root.querySelector('[data-secant-line]'),point=root.querySelector('[data-secant-point]'),output=root.querySelector('[data-secant-output]');
 function draw(){
  const h=Number(slider.value),slope=2+h;
  point.setAttribute('cx',String(50+210*(1+h)));
  point.setAttribute('cy',String(290-36*(1+h)**2));
  line.setAttribute('y1',String(290-36*(slope*(0.5-1)+1)));
  line.setAttribute('y2',String(290-36*(slope*(2.4-1)+1)));
  output.textContent=`h = ${h.toFixed(2)}；割线斜率 = ${slope.toFixed(2)}；切线斜率 = 2`;
 }
 slider.addEventListener('input',draw);draw();
});
document.querySelectorAll('.surface-explorer').forEach(root=>{
 const buttons=[...root.querySelectorAll('[data-surface]')];
 buttons.forEach(b=>b.addEventListener('click',()=>activate(buttons,b,root.querySelectorAll('.surface-panel'),p=>p.id===b.dataset.surface)));
});
document.querySelectorAll('.step-explorer').forEach(root=>{
 const buttons=[...root.querySelectorAll('[data-step]')];
 buttons.forEach(b=>b.addEventListener('click',()=>activate(buttons,b,root.querySelectorAll('[data-panel]'),p=>p.dataset.panel===b.dataset.step)));
});
const objectButtons=[...document.querySelectorAll('[data-object]')];
objectButtons.forEach(b=>b.addEventListener('click',()=>activate(objectButtons,b,document.querySelectorAll('[data-object-panel]'),p=>p.dataset.objectPanel===b.dataset.object)));
document.querySelectorAll('[data-catalog]').forEach(root=>{
 const buttons=[...root.querySelectorAll('[data-filter]')],input=root.querySelector('input'),items=[...root.querySelectorAll('.catalog-item')];
 let selected='all';
 function update(){
  const query=input.value.trim().toLowerCase();let visible=0;
  items.forEach(item=>{const show=(selected==='all'||item.dataset.category===selected)&&item.dataset.search.toLowerCase().includes(query);item.hidden=!show;if(show)visible++;});
  root.querySelector('.empty-state').hidden=visible>0;
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===selected)));
 }
 buttons.forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.filter;update();}));input.addEventListener('input',update);
 const initial=new URLSearchParams(location.search).get('filter');if(buttons.some(b=>b.dataset.filter===initial)){selected=initial;update();}
});
const article=document.querySelector('.article-content'),progress=document.querySelector('.reading-progress');
if(article){
 const headings=[...article.querySelectorAll('section[id]')],links=[...document.querySelectorAll('.article-aside nav a')];
 let scheduled=false;
 function updateReading(){
  scheduled=false;const top=article.getBoundingClientRect().top+window.scrollY;const distance=article.offsetHeight-window.innerHeight+120;
  progress.style.width=Math.max(0,Math.min(100,(window.scrollY-top+120)/Math.max(1,distance)*100))+'%';
  let current=headings[0]?.id;for(const section of headings){if(section.getBoundingClientRect().top<160)current=section.id;}
  links.forEach(a=>{const active=a.getAttribute('href')==='#'+current;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
 }
 addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateReading);}},{passive:true});addEventListener('resize',updateReading);updateReading();
}
