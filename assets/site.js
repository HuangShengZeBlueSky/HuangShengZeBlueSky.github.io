const search=document.getElementById('note-search');
if(search){search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let shown=0;document.querySelectorAll('.filter-item').forEach(el=>{const match=el.textContent.toLowerCase().includes(q);el.hidden=!match;if(match)shown++;});document.getElementById('no-results').hidden=shown!==0;});}

const routes={
 harness:{name:'AutoHarness',title:'让“已查到号源”和“已完成办理”成为不同的进度。',description:'如果问题在于进度没有被稳定利用，可以让程序记录真实回执，把当前状态交给模型，并在工具执行前检查必要条件。',change:'改变的是外围运行程序，做事模型的权重保持固定。',url:'/research/harness.html'},
 sft:{name:'AutoSFT',title:'补充在相应情境下，应该怎样行动的示范。',description:'如果模型缺少处理预约状态冲突的正确经验，就准备不同的客户反应，让教师模型实际交互，筛选出正确回复与工具动作，再用于监督微调。',change:'改变的是训练数据；学习这些示范后，得到新的模型参数。',url:'/projects/sft.html'},
 reward:{name:'RewardWeaver / AutoRL',title:'让训练更重视当前反复限制任务成功的行为。',description:'先从失败中找出瓶颈，再选择对应的过程奖励。例如模型总是没有回应客户的关切，就让训练对这一行为提供更具体的反馈。',change:'改变的是训练采用的奖励，策略模型通过强化学习更新。',url:'/research/reward.html'}
};
const tabs=[...document.querySelectorAll('[data-route]')];
function chooseRoute(button){
 const route=routes[button.dataset.route];
 tabs.forEach(tab=>{const active=tab===button;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;});
 for(const key of ['name','title','description','change'])document.getElementById('route-'+key).textContent=route[key];
 document.getElementById('route-link').href=route.url;
 document.getElementById('route-panel').setAttribute('aria-labelledby',button.id);
}
tabs.forEach((button,index)=>{
 button.tabIndex=button.getAttribute('aria-selected')==='true'?0:-1;
 button.addEventListener('click',()=>chooseRoute(button));
 button.addEventListener('keydown',event=>{
  let next;
  if(event.key==='ArrowRight')next=(index+1)%tabs.length;
  else if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;
  else if(event.key==='Home')next=0;
  else if(event.key==='End')next=tabs.length-1;
  if(next!==undefined){event.preventDefault();chooseRoute(tabs[next]);tabs[next].focus();}
 });
});
