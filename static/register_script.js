
// JavaScript logic to show/hide forms based on the selected option
const selectIdentity = document.getElementById('selectIdentity');
const form1 = document.getElementById('customer-form');
const form2 = document.getElementById('agent-form');
const form3 = document.getElementById('staff-form');

// Add event listener to the select element
selectIdentity.addEventListener('change', function handleChange(event) {
 
    // Show the selected form based on the selected option
    console.log(event.target.value);
    if (event.target.value === 'customer') {
    form1.style.display = 'inline';
    form2.style.display = "none";
    form3.style.display = "none";
    } else if (event.target.value === 'booking_agent') {
    form2.style.display = 'inline';
    form1.style.display = "none";
    form3.style.display = "none";
    } else if (event.target.value === 'airline_staff') {
    form3.style.display ='inline';
    form1.style.display = "none";
    form2.style.display = "none";
    }
});
