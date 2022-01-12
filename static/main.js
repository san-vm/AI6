var headers = {
	headers: {
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	},
	method: "POST",
}
var loginSub = document.querySelector("#loginSub")
var token = '';

loginSub.addEventListener("click", (event) => {
	event.preventDefault()
	var username = document.querySelector("#username").value
	var password = document.querySelector("#password").value
	var body = {
		"username": username,
		"password": password
	}
	headers["body"] = JSON.stringify(body)

	fetch("login", headers)
		.then((res) => res.text())
		.then((res) => console.log(res))
})

var testbt = document.querySelector("#testbt")
testbt.addEventListener("click", () => {
	var headers = {
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		},
		method: "POST",
	}

	fetch("uname", headers)
		.then((res) => res.json())
		.then((res) => console.log(res))
})