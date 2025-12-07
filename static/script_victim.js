document.getElementById("send").addEventListener("click", () => {
    fetch("/victim/send")
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").textContent =
                "Prediction: " + data.prediction;
        })
        .catch(err => console.error(err));
});