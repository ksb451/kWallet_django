const serchField = document.querySelector('#searchField');

const tableOutput = document.querySelector(".table-output");
tableOutput.style.display = "none";

const paginationContainer = document.querySelector(".pagination-container");

const appTable = document.querySelector(".app-table");
const noResult = document.querySelector(".no-search-result");
const tbody = document.querySelector(".output-table-body");
serchField.addEventListener("keyup", (e)=>{
	const searchValue = e.target.value;
	if(searchValue.trim().length > 0)
	{
		while (tbody.firstChild){
			tbody.removeChild(tbody.firstChild);
		}
		console.log(searchValue);
		fetch("search-incomes",{
		body:JSON.stringify({
			searchText:searchValue}),
		method:"POST",
		})
		.then(res=>res.json())
		.then((data)=>{
			console.log("data",data);
			appTable.style.display ="none";

			paginationContainer.style.display='none';
			noResult.style.display ="none";
			tableOutput.style.display="block";
			if(data.length===0)
			{
				tableOutput.style.display = 'none';
				noResult.style.display ="block";
			}
			else{
				data.forEach(itam=>{
					tbody.innerHTML+=`
						<tr>
						<td>${itam.amount}</td>
						<td>${itam.source}</td>
						<td>${itam.description}</td>
						<td>${itam.date}</td>
						<td></td>
						</tr>
						`
				});
			}
		});
	}
	else{
		console.log(0);
		noResult.style.display ="none";
		tableOutput.style.display="none";
		appTable.style.display ="block";
		paginationContainer.style.display='block';
	}

});