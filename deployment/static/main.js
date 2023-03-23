async function fetchAsync(url) {
    let response = await fetch(url);
    let data = await response.json();
    return data;
}

function populate_categorical_list(category){
    fetchAsync('/get_category_values/' + category).then(response => {
        list = document.getElementById(category);
        response.forEach(element => {
            htmlElement = document.createElement("option");
            htmlElement.value = element;
            htmlElement.innerHTML = element;
            list.append(htmlElement);
        });
    });
}

async function predict(event){
    event.preventDefault(); // This prevents the default behaviour of the form
    document.getElementById('prediction').innerHTML = "Predicting...";

    const form = event.currentTarget; // This is the form
    const action_url = form.action; // This is the action url

    try {
        const formData = new FormData(form);
        const response = await fetch(action_url, {method: 'POST', body: formData});
        const data = await response.json();

        document.getElementById('prediction').innerHTML = "Predicted arrival delay: " + data.predicted.toFixed(2) + " minutes";
        console.log(response)
        if (!response.ok) {
            throw new Error(response.statusText);
        }

    } catch (error) {
        console.log("Error" + error);
    }

    return true;
}


window.onload = function() {
    document.getElementsByTagName('form')[0].addEventListener('submit', predict);
    populate_categorical_list('Airline');
    populate_categorical_list('Dest');
    populate_categorical_list('DestCityName');
    populate_categorical_list('DestState');
    populate_categorical_list('Origin');
    populate_categorical_list('OriginCityName');
    populate_categorical_list('OriginState');
}