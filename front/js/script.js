const API_URL = "http://localhost:5000/api/nutrition";
let editingId = null;

// Carrega a lista completa de pacientes
async function loadPatients() {
  try {
    const response = await fetch(`${API_URL}/`);
    if (!response.ok) throw new Error("Erro ao carregar pacientes");
    const patients = await response.json();
    renderTable(patients);
  } catch (err) {
    console.error("Erro:", err);
  }
}

// Função CENTRAL para exibir dados na tabela (COM A CORREÇÃO)
function renderTable(patients) {
  const tbody = document.querySelector("#patientsTable tbody");
  
  // A LINHA MAIS IMPORTANTE: Apaga todo o conteúdo anterior da tabela
  tbody.innerHTML = ""; 

  // Se a lista de pacientes estiver vazia, mostra uma mensagem
  if (patients.length === 0) {
    tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">Nenhum resultado encontrado.</td></tr>';
    return;
  }

  // Adiciona as novas linhas com base nos dados recebidos
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

// --- section search ---
async function handleSearch() {
  const searchTerm = document.getElementById("search").value.trim();
  if (!searchTerm) {
    loadPatients();
    return;
  }
  if (isNaN(searchTerm)) {
    await searchPatientsByName(searchTerm);
  } else {
    await searchPatientById(searchTerm);
  }
}

async function searchPatientById(id) {
  try {
    const response = await fetch(`${API_URL}/${id}`);
    if (response.status === 404) {
      renderTable([]); // Envia um array vazio para limpar a tabela e mostrar msg
      return;
    }
    if (!response.ok) throw new Error("Erro ao buscar paciente por ID");
    const patient = await response.json();
    renderTable([patient]); // Envia o resultado para a função de renderização
  } catch (err) {
    console.error(err);
    renderTable([]);
  }
}

async function searchPatientsByName(name) {
  try {
    const response = await fetch(`${API_URL}/?name=${encodeURIComponent(name)}`);
    if (!response.ok) throw new Error("Erro ao buscar pacientes por nome");
    const patients = await response.json();
    // const exactMatches = patients.filter(p => p.name.toLowerCase() === name.toLowerCase());
    // renderTable(exactMatches);
    renderTable(patients); // Envia os resultados para a função de renderização
  } catch (err) {
    console.error(err);
    renderTable([]);
  }
}

// Eventos do botão e campo de busca
document.getElementById("search-btn").addEventListener("click", handleSearch);
document.getElementById("search").addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    handleSearch();
  }
});

// Carrega a lista inicial ao abrir a página
loadPatients();

//Configuração do slider
document.addEventListener('DOMContentLoaded', () => {
    const sliderWrapper = document.querySelector('.slider-wrapper');
    // Se não encontrar o slider na página, não faz nada
    if (!sliderWrapper) return;

    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    let currentIndex = 0;
    const totalSlides = slides.length;

    // Função para mover o slider para um slide específico
    function goToSlide(index) {
        // Move o wrapper horizontalmente
        sliderWrapper.style.transform = `translateX(-${index * 100}%)`;
    }

    // Evento para o botão "Próximo"
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalSlides; // O '%' faz o slider voltar ao início
        goToSlide(currentIndex);
    });

    // Evento para o botão "Anterior"
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides; // Lógica para voltar para o último slide
        goToSlide(currentIndex);
    });

    // Opcional: transição automática de slides
    setInterval(() => {
        nextBtn.click();
    }, 15000); // Muda de slide a cada 5 segundos
});


//configuração do botão de voltar ao topo
window.addEventListener("scroll", function () {
  if (window.pageYOffset > 200) {
    document.querySelector(".back-to-top-button").style.display = "block";
  } else {
    document.querySelector(".back-to-top-button").style.display = "none";
  }
});

document
  .querySelector(".back-to-top-button a")
  .addEventListener("click", function (e) {
    e.preventDefault(); // Prevent default anchor link behavior
    window.scrollTo({
      top: 0, // Scroll to top of page
      behavior: "smooth", // Smooth scrolling
    });
  });