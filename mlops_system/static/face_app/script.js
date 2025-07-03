let facemeshModel;
let imgElement;
let predictions = [];
const overlay = document.getElementById('overlay');
const ctx = overlay.getContext('2d');
const saveBtn = document.getElementById('saveBtn');

document.getElementById('imageUpload').addEventListener('change', handleImage);
saveBtn.addEventListener('click', () => {
  if (predictions.length) {
    localStorage.setItem('facemesh', JSON.stringify(predictions));
    alert('Landmarks saved to localStorage');
  }
});

function handleImage(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    imgElement = new Image();
    imgElement.onload = () => {
      overlay.width = imgElement.width;
      overlay.height = imgElement.height;
      ctx.drawImage(imgElement, 0, 0);
      loadModel();
    };
    imgElement.src = ev.target.result;
  };
  reader.readAsDataURL(file);
}

function loadModel() {
  if (facemeshModel) {
    predict();
  } else {
    facemeshModel = ml5.facemesh(modelReady);
  }
}

function modelReady() {
  predict();
}

function predict() {
  facemeshModel.predict(imgElement, (err, results) => {
    if (err) return console.error(err);
    predictions = results;
    drawKeypoints();
    computeHeadPose();
  });
}

function drawKeypoints() {
  ctx.drawImage(imgElement, 0, 0);
  ctx.fillStyle = 'red';
  predictions.forEach(pred => {
    pred.scaledMesh.forEach(pt => {
      ctx.fillRect(pt[0], pt[1], 2, 2);
    });
  });
}

function computeHeadPose() {
  if (!predictions.length) return;
  const pts = predictions[0].scaledMesh;
  const leftEar = pts[234];
  const rightEar = pts[454];
  const forehead = pts[10];
  const nose = pts[1];

  const yaw = Math.atan2(rightEar[1] - leftEar[1], rightEar[0] - leftEar[0]);
  const pitch = Math.atan2(nose[2] - forehead[2], nose[1] - forehead[1]);

  addHairModel(yaw, pitch, forehead);
}

function addHairModel(yaw, pitch, forehead) {
  const container = document.getElementById('threeContainer');
  container.innerHTML = '';
  const width = overlay.width;
  const height = overlay.height;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.z = 500;

  const renderer = new THREE.WebGLRenderer({ alpha: true });
  renderer.setSize(width, height);
  container.appendChild(renderer.domElement);

  const texture = new THREE.Texture(imgElement);
  texture.needsUpdate = true;
  const plane = new THREE.Mesh(
    new THREE.PlaneGeometry(width, height),
    new THREE.MeshBasicMaterial({ map: texture })
  );
  scene.add(plane);

  const hair = new THREE.Mesh(
    new THREE.ConeGeometry(120, 200, 32),
    new THREE.MeshPhongMaterial({ color: 0x332200 })
  );
  hair.position.set(forehead[0] - width / 2, -forehead[1] + height / 2 + 80, 50);
  hair.rotation.y = yaw;
  hair.rotation.x = pitch;
  scene.add(hair);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(0, 0, 1);
  scene.add(light);

  renderer.render(scene, camera);
}
