/*
Código para agregar un año cuando se selecciona una fecha de inicio
Página: /web/1/issuance/insurance/vehicle/create_policy/quotation_premium/1/
Para la creación de una emisión de póliza
*/
const initialValidity = document.querySelector('#id_initial_validity');
const finalValidity = document.querySelector('#id_final_validity');

initialValidity.addEventListener('change', () => {
	const date = new Date(initialValidity.value);
	date.setFullYear(date.getFullYear() + 1);
	finalValidity.value = date.toISOString().slice(0, 10);
});

/* Fin de código para agregar un año cuando se selecciona una fecha de inicio */
