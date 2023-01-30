const container = document.querySelector("#results");

const COLORS = {
  base: {
    'white': [255, 255, 255],
    'black': [0, 0, 0],
  },
  primary: {
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
  },
  secondary: {
    'yellow': [255, 255, 0],
    'magenta': [255, 0, 255],
    'cyan': [0, 255, 255],
  },
  tertiary: {
    'orange': [255, 165, 0],
    'purple': [128, 0, 128],
    'brown': [165, 42, 42],
  },
  all: {
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
    'yellow': [255, 255, 0],
    'magenta': [255, 0, 255],
    'cyan': [0, 255, 255],
    'orange': [255, 165, 0],
    'purple': [128, 0, 128],
    'brown': [165, 42, 42],
  },
}

// read results.csv and display them
// csv format: background color, best color, contrast, compliance
function fetchResults(file) {
  fetch(
    file
  )
    .then((response) => response.text())
    .then((text) => {
      container.innerHTML = "<h2>Loading...</h2>";

      const lines = text.split("\n");
      const results = [];
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i];
        const values = line.split(",");
        const color = values[0]
        const bestColor = values[1];
        const contrast = parseFloat(values[2]);
        const compliance = values[3];
        results.push({ color, bestColor, contrast, compliance });
      }

      container.innerHTML = "";
      for (let i = 0; i < results.length - 1; i++) {
        const result = results[i];
        const div = document.createElement("div");
        div.style.backgroundColor = result.color;
        div.style.color = result.bestColor;
        div.style.textAlign = "center";
        div.innerHTML = `${result.color}<br>
          ${result.contrast.toFixed(2)}<br>
          <br> ${result.compliance}`;
        container.appendChild(div);
      }
    })
    .catch((error) => console.log(error));
}

function fetchRapport(file) {
  fetch(
    file
  )
    .then((response) => response.json())
    .then((text) => {
      contrast.innerHTML = "";
      compliance.innerHTML = "";
      bestColor.innerHTML = "";
      contrastBarInit.style.background = `linear-gradient(to right, #004e98 ${(text.contrast.min - 1) * 100 / 21}%,#ff6700 ${(text.contrast.min - 1) * 100 / 21}%,#ff6700 ${text.contrast.max * 100 / 21}%,#004e98 ${text.contrast.max * 100 / 21
        }%)`;
      contrast.innerHTML = text.contrast.min + " - " + text.contrast.max;
      compliance.innerHTML = text.compliance.AAA + " are AAA ( " + (text.compliance.AAA / text.colors.tested * 100).toFixed(2) + "% )" + "<br>" + text.compliance.AA + " are AA ( " + (text.compliance.AA / text.colors.tested * 100).toFixed(2) + "% )" + "<br>" + text.compliance.None + " fail ( " + (text.compliance.None / text.colors.tested * 100).toFixed(2) + "% )";
      for (color in text.bestColors) {
        bestColor.innerHTML += color + " : " + text.bestColors[color] + "( " + (text.bestColors[color] / (text.colors.tested) * 100).toFixed(2) + "% ) <br>";
      }
    }
    )
    .catch((error) => console.log(error));
}


previewFromSelect = () => {
  const select = document.getElementById("colorType");
  document.querySelector("[data-color-type]").innerHTML = "";

  Object.keys(COLORS[select.value]).forEach((color) => {
    const preview = document.createElement("span");
    preview.style.backgroundColor = color;

    document.querySelector("[data-color-type]").appendChild(preview);
  });
}


getColorStep = () => {
  const range = document.getElementById("colorStep");
  return range.value;
}

getColFromColorStep = () => {
  const range = document.getElementById("colorStep");
  switch (range.value) {
    case "64":
      return 4;
    case "32":
      return 8;
    case "16":
      return 16;
    case "8":
      return 32;
    case "4":
      return 64;
  }
}

fetchData = () => {
  const fileName = './src/files/luminance_' + document.getElementById("colorType").value + '_' + getColorStep() + '.csv';
  container.className = "col-" + getColFromColorStep();
  container.className = "col-" + getColFromColorStep(); fetchResults(fileName);
  fetchRapport('./src/files/luminance_' + document.getElementById("colorType").value + '_' + getColorStep() + '.json');
}


document.getElementById("colorType").addEventListener("change", function (e) {
  fetchData();
  previewFromSelect();
});

document.getElementById("colorStep").addEventListener("change", function (e) {
  fetchData();
});

fetchData();
previewFromSelect();
