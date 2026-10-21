module.exports=async(page)=>{
  await page.waitForFunction(()=>document.querySelector('#train-prog')&&document.querySelector('#train-prog').textContent.includes('ready'),{timeout:120000});
  await page.type('#msg','Congratulations you won a free iPhone, click the link in my bio to claim now');
  await page.click('#analyze');
  await page.waitForSelector('#result:not(.hidden)',{timeout:20000});
  const v1=await page.$eval('#verdict',e=>e.textContent);
  if(!/Spam/.test(v1))throw new Error('spam not detected: '+v1);
  await page.evaluate(()=>{document.getElementById('msg').value='';document.getElementById('prob-num').textContent='—'});
  await page.type('#msg','I tried this recipe tonight and my kids actually ate their vegetables, thank you');
  await page.click('#analyze');
  await page.waitForFunction(()=>document.querySelector('#prob-num').textContent!=='—',{timeout:20000});
  const v2=await page.$eval('#verdict',e=>e.textContent);
  if(!/genuine/.test(v2))throw new Error('genuine not detected: '+v2);
  const acc=await page.$eval('#m-acc',e=>e.textContent);
  return `spam+genuine detected, CV acc=${acc}`;
};
