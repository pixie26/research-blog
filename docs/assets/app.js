(() => {
  // Keep old shared market anchors usable after the single-page archive becomes the blog home.
  if (location.pathname === '/research-blog/' && ['#us','#china-hk','#japan','#korea','#cross-market'].includes(location.hash)) {
    location.replace('/research-blog/archive/jpm-week-20261009/' + location.hash); return;
  }
  const search = document.getElementById('search');
  if (search) search.addEventListener('input', () => {
    const q=search.value.trim().toLocaleLowerCase(), cards=[...document.querySelectorAll('.post-card')];
    let count=0;
    cards.forEach(card => { const show=!q || card.dataset.search.toLocaleLowerCase().includes(q); card.hidden=!show; if(show)count++; });
    document.getElementById('empty-search').hidden=count!==0;
    document.getElementById('search-status').textContent=q ? `找到 ${count} 篇文章` : '';
  });
  const copy=document.getElementById('copy-link');
  if(copy) copy.addEventListener('click',async()=>{
    const status=document.getElementById('copy-status');
    const canonical=document.querySelector('link[rel="canonical"]').href;
    try { await navigator.clipboard.writeText(canonical); status.textContent='链接已复制'; }
    catch { status.textContent='请从地址栏复制本页链接'; }
  });
  if(matchMedia('(max-width:620px)').matches){const d=document.querySelector('.toc details'); if(d)d.open=false;}
})();
