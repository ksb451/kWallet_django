// console.log("register working")
const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid-feedback");

const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");

const submitBTN = document.querySelector(".submit-btn");

const handleToggleInput=(e)=>{
	if(showPasswordToggle.textContent === 'SHOW'){
		showPasswordToggle.textContent = 'HIDE';
		passwordField.setAttribute("type","text");
	}
	else{
		showPasswordToggle.textContent = 'SHOW';
		passwordField.setAttribute("type","password");
	}

}

showPasswordToggle.addEventListener('click', handleToggleInput);


usernameField.addEventListener("keyup",(e)=>{
	console.log('77777',7777);
	const usernameval = e.target.value;
	usernameSuccessOutput.style.display= "block";
	usernameSuccessOutput.textContent = `Checking ${usernameval}`;

	usernameField.classList.remove('is-invalid');
	feedBackArea.style.display= "none"

	console.log('username', usernameval);
	fetch("/authentication/validate-username",{
		body:JSON.stringify({
			username:usernameval}),
		method:"POST",
		})
	.then(res=>res.json())
	.then((data)=>{
		console.log("data",data)
		usernameSuccessOutput.style.display= "none";
		if(data.username_error){
			submitBTN.setAttribute('disabled','disabled');
			submitBTN.disabled = true;
			usernameField.classList.add('is-invalid');
			feedBackArea.style.display= "block"
			feedBackArea.innerHTML=`<p>${data.username_error}</p>`
		}
		else{
			submitBTN.removeAttribute('disabled');
		}
	});
	});

const emailField = document.querySelector("#emailField");
const emailfeedBackArea = document.querySelector(".invalid-feedback-email");
emailField.addEventListener("keyup",(e)=>{
	console.log('77777',7777);
	const emailval = e.target.value;

	emailSuccessOutput.style.display= "block";
	emailSuccessOutput.textContent = `Checking ${emailval}`;

	emailField.classList.remove('is-invalid');
	emailfeedBackArea.style.display= "none"

	console.log('email', emailval);
	fetch("/authentication/validate-email",{
		body:JSON.stringify({
			email:emailval}),
		method:"POST",
		})
	.then(res=>res.json())
	.then((data)=>{
		console.log("data",data)
		emailSuccessOutput.style.display= "none";
		if(data.email_error){
			submitBTN.setAttribute('disabled','disabled');
			submitBTN.disabled = true;
			emailField.classList.add('is-invalid');
			emailfeedBackArea.style.display= "block"
			emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`
		}
		else{
			submitBTN.removeAttribute('disabled');
		}
	});
	});
