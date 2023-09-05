document.getElementById('carbonForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // Get input values
    const food = parseFloat(document.getElementById('food').value);
    const electricityUsage = parseFloat(document.getElementById('electricity').value);
    const gasUsage = parseFloat(document.getElementById('gas').value);
    const fuelUsage = parseFloat(document.getElementById('fuel').value);
    // Conversion factors (adjust these based on your specific calculation)
    const foodfactor=0;
    const electricityFactor = 0.5; // kg CO2e per kWh
    const gasFactor = 2.2; // kg CO2e per therm
    const fuelFactor = 2.5; // kg CO2e per gallon
    // Calculate total carbon footprint
    const totalCarbonFootprint =(foodfactor*food)+ (electricityUsage * electricityFactor) + (gasUsage * gasFactor) + (fuelUsage * fuelFactor);
    // Update result on the page
    const resultElement = document.getElementById('carbonResult');
    resultElement.textContent = totalCarbonFootprint.toFixed(2);
    // Show the result section
    document.getElementById('resultSection').style.display = 'block';
});
