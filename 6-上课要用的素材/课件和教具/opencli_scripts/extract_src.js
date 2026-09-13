(() => {
  const imgs = [...document.querySelectorAll('[data-message-author-role=assistant] img')];
  if (!imgs.length) return JSON.stringify({err:'no-img'});
  const out = imgs.slice(0,4).map(i => ({src: i.src, w: i.naturalWidth, h: i.naturalHeight}));
  return JSON.stringify({ok:true, count: imgs.length, imgs: out});
})()
