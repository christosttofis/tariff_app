const _base = window.location.protocol === 'file:' ? 'http://localhost:8000' : '';
const params = new URLSearchParams(window.location.search);
const token  = params.get('token');
const setup  = params.get('setup') === '1';

if(!token){
  document.getElementById('form-wrap').style.display = 'none';
  document.getElementById('expired-msg').style.display = 'block';
  if(setup){
    document.getElementById('expired-title').textContent = 'Invitation expired';
    document.getElementById('expired-body').textContent = 'This invitation link has expired or is invalid. Please contact your CERA administrator to request a new one.';
  }
}

// Setup-mode: show account-activation wording instead of reset-password wording
if(setup){
  document.getElementById('form-title').textContent = 'Set up your account';
  document.getElementById('form-sub').textContent = 'Welcome! Please create a password to activate your Supplier Portal account.';
  document.getElementById('submit-btn').textContent = 'Activate account';
}

// Detect which portal to link back to based on referrer or a param
const portal = params.get('portal') || 'admin';
document.querySelector('.back-link').href = portal === 'supplier' ? 'supplier.html' : 'admin.html';
document.querySelector('.back-link').textContent = portal === 'supplier'
  ? '← Back to Supplier sign in'
  : '← Back to Admin sign in';

async function doReset(){
  const pw1 = document.getElementById('pw1').value;
  const pw2 = document.getElementById('pw2').value;
  const msg = document.getElementById('msg');
  msg.textContent = ''; msg.className = 'msg';

  const isStrong = pw1.length >= 8 && /[A-Za-z]/.test(pw1) && /[0-9]/.test(pw1) && /[^A-Za-z0-9]/.test(pw1);
  if(!isStrong){
    msg.textContent = 'Password must be at least 8 characters and include a letter, a number, and a symbol.';
    msg.className = 'msg err'; return;
  }
  if(pw1 !== pw2){
    msg.textContent = 'Passwords do not match.';
    msg.className = 'msg err'; return;
  }

  const btn = document.getElementById('submit-btn');
  btn.disabled = true; btn.textContent = 'Saving…';

  try{
    const resp = await fetch(_base + '/api/auth/reset-password', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({token, password: pw1})
    });
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      const successMsg = setup
        ? '<h2 style="color:var(--green);margin-bottom:10px">Account activated</h2><p style="font-size:13px;color:var(--text2);line-height:1.7">Your account is ready. You can now sign in to the Supplier Portal.</p>'
        : '<h2 style="color:var(--green);margin-bottom:10px">Password updated</h2><p style="font-size:13px;color:var(--text2);line-height:1.7">Your password has been changed. You can now sign in with your new password.</p>';
      document.getElementById('form-wrap').innerHTML = successMsg;
    } else {
      msg.textContent = data.detail || 'Something went wrong. The link may have expired.';
      msg.className = 'msg err';
      if(resp.status === 400 && (data.detail||'').toLowerCase().includes('expired')){
        document.getElementById('form-wrap').style.display = 'none';
        document.getElementById('expired-msg').style.display = 'block';
      }
      btn.disabled = false; btn.textContent = 'Set new password';
    }
  }catch(e){
    msg.textContent = 'Network error — please try again.';
    msg.className = 'msg err';
    btn.disabled = false; btn.textContent = 'Set new password';
  }
}

// Submit on Enter
document.addEventListener('keydown', e => {
  if(e.key === 'Enter' && token) doReset();
});

document.getElementById('submit-btn').addEventListener('click', doReset);
