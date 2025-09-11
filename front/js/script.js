const API_URL = "http://localhost:5000/api/nutrition"; // Remove a barra final da URL base

let editingId = null;

// Carregar pacientes
async function loadPatients() {
  try {
    // GET: Adiciona a barra final para o endpoint de lista
    const response = await fetch(`${API_URL}/`);
    if (!response.ok) throw new Error("Erro ao carregar pacientes");
    const patients = await response.json();

    const tbody = document.querySelector("#patientsTable tbody");
    tbody.innerHTML = ""; // limpa antes de preencher

    patients.forEach((p) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${p.id}</td>
        <td>${p.name}</td>
        <td>${p.height}</td>
        <td>${p.weight}</td>
        <td>${p.age}</td>
        <td>${p.gender}</td>
        <td>${p.activity_level}</td>
        <td>${p.calories}</td>
        <td>${p.body_percentage}</td>
        <td>
          <button onclick="editPatient(${p.id}, '${p.name}', ${p.height}, ${p.weight}, ${p.age}, '${p.gender}', '${p.activity_level}', ${p.calories}, ${p.body_percentage})">✏️ Editar</button>
          <button onclick="deletePatient(${p.id})">🗑️ Excluir</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Erro:", err);
  }
}

// Adicionar/Editar paciente
document.querySelector("#ntrForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const patient = {
    name: document.querySelector("#name").value,
    height: parseFloat(document.querySelector("#height").value),
    weight: parseFloat(document.querySelector("#weight").value),
    age: parseInt(document.querySelector("#age").value, 10),
    gender: document.querySelector("#gender").value,
    activity_level: document.querySelector("#activity_level").value,
    calories: parseInt(document.querySelector("#calories").value, 10),
    body_percentage: parseFloat(document.querySelector("#body_percentage").value),
  };

  try {
    if (editingId) {
      const response = await fetch(`${API_URL}/${editingId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patient),
      });
      if (!response.ok) throw new Error("Erro ao atualizar paciente");
      editingId = null;
      document.querySelector("#formTitle").innerText = "Adicione seus dados";
      document.querySelector("#cancelEdit").style.display = "none";
    } else {  
      const response = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patient),
      });
      if (!response.ok) throw new Error("Erro ao adicionar paciente");
    }

    document.querySelector("#ntrForm").reset();
    loadPatients();
  } catch (err) {
    console.error("Erro:", err);
  }
});

// Cancelar edição
document.querySelector("#cancelEdit").addEventListener("click", () => {
  editingId = null;
  document.querySelector("#ntrForm").reset();
  document.querySelector("#formTitle").innerText = "Adicione seus dados";
  document.querySelector("#cancelEdit").style.display = "none";
});

// Editar paciente
function editPatient(id, name, height, weight, age, gender, activity_level, calories, body_percentage) {
  editingId = id;
  document.querySelector("#name").value = name;
  document.querySelector("#height").value = height;
  document.querySelector("#weight").value = weight;
  document.querySelector("#age").value = age;
  document.querySelector("#gender").value = gender;
  document.querySelector("#activity_level").value = activity_level;
  document.querySelector("#calories").value = calories;
  document.querySelector("#body_percentage").value = body_percentage;

  document.querySelector("#formTitle").innerText = "Editar Paciente";
  document.querySelector("#cancelEdit").style.display = "inline";
}

// Excluir paciente
async function deletePatient(id) {
  if (!confirm("Tem certeza que deseja excluir este paciente?")) return;
  try {
    const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Erro ao excluir paciente");
    loadPatients();
  } catch (err) {
    console.error("Erro:", err);
  }
}

// carregar lista ao abrir
loadPatients();