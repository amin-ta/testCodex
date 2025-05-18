let token = localStorage.getItem('token') || '';

document.addEventListener('DOMContentLoaded', () => {
  if (token) document.getElementById('token').value = token;
  listDatasets();
});

function setToken() {
  token = document.getElementById('token').value;
  localStorage.setItem('token', token);
  alert('Token saved');
}

async function uploadDataset() {
  const name = document.getElementById('datasetName').value;
  const file = document.getElementById('datasetFile').files[0];
  if (!name || !file) {
    alert('name and file required');
    return;
  }
  const form = new FormData();
  form.append('name', name);
  form.append('file', file);
  const res = await fetch('/upload', {
    method: 'POST',
    headers: { 'Authorization': token },
    body: form
  });
  const data = await res.json();
  alert(JSON.stringify(data));
  listDatasets();
}

async function listDatasets() {
  const res = await fetch('/datasets', {
    headers: { 'Authorization': token }
  });
  const data = await res.json();
  const list = document.getElementById('datasets');
  const select = document.getElementById('trainDataset');
  list.innerHTML = '';
  select.innerHTML = '';
  if (!data.datasets) return;
  data.datasets.forEach(d => {
    const li = document.createElement('li');
    li.textContent = d;
    list.appendChild(li);
    const opt = document.createElement('option');
    opt.value = d;
    opt.textContent = d;
    select.appendChild(opt);
  });
}

async function trainDataset() {
  const dataset = document.getElementById('trainDataset').value;
  const val = parseFloat(document.getElementById('valSplit').value);
  const res = await fetch(`/datasets/${dataset}/train`, {
    method: 'POST',
    headers: {
      'Authorization': token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ val_split: val })
  });
  const data = await res.json();
  alert('Training results stored in ' + data.result_dir);
}
