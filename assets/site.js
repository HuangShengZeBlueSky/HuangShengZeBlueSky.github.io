const search=document.getElementById('note-search');
if(search){search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let shown=0;document.querySelectorAll('.filter-item').forEach(el=>{const match=el.textContent.toLowerCase().includes(q);el.hidden=!match;if(match)shown++;});document.getElementById('no-results').hidden=shown!==0;});}
