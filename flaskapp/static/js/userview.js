function togglePopUp(popUpId) {
    var popUp = document.getElementById(popUpId);
    if (popUp.style.display === 'none') {
        popUp.style.display = 'block';
    } else {
        popUp.style.display = 'none';
    }
}