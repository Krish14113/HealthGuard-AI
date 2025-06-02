async function predictDisease() {
  const symptomsInput = document.getElementById("symptoms").value;

  if (!symptomsInput.trim()) {
    alert("Please enter symptoms.");
    return;
  }

  const responseBox = document.getElementById("result");
  responseBox.innerHTML = "🔄 Processing...";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ symptoms: symptomsInput })
    });

    const data = await response.json();

    if (data.error) {
      responseBox.innerHTML = `<p style="color:red;">❌ ${data.error}</p>`;
    } else {
      const { disease, description, precautions } = data;

      responseBox.innerHTML = `
        <h3>🔍 Predicted Disease: ${disease}</h3>
        <p><strong>📄 Description:</strong> ${description}</p>
        <p><strong>🩺 Precautions:</strong></p>
        <ul>${precautions.map(item => `<li>${item}</li>`).join("")}</ul>
      `;
    }
  } catch(error => {
  if (error.response && error.response.status === 400) {
    alert(error.response.data.error || "Invalid input. Please enter valid symptoms.");
  } else {
    alert("Prediction failed. Make sure the backend is running.");
  }
  console.error(error);
});

