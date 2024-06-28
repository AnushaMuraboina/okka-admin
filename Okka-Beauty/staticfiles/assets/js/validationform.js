
	
	function validate_password() {

		var pass = document.getElementById('password').value;
		var confirm_pass = document.getElementById('confirm_password').value;
		if (pass != confirm_pass) {
			document.getElementById('wrong_pass_alert').style.color = '#DC3545';
			document.getElementById('wrong_pass_alert').innerHTML
			= '☒ Use same password';
			document.getElementById('create').disabled = true;
			document.getElementById('create').style.opacity = (0.4);
		}else if(confirm_pass == ""){
			document.getElementById('wrong_pass_alert').style.color = '#DC3545';
			document.getElementById('wrong_pass_alert').innerHTML
			= '☒ Please enter confirm Password';
			document.getElementById('create').disabled = true;
			document.getElementById('create').style.opacity = (0.4);
		} else {
			document.getElementById('wrong_pass_alert').style.color = 'green';
			document.getElementById('wrong_pass_alert').innerHTML =
			'Password Matched';
			document.getElementById('create').disabled = false;
			document.getElementById('create').style.opacity = (1);
		}
		validateForm();
		}
	
	
	function validateStrongPassword(password) {
	  var re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;
	  return re.test(password);
	}


	function validate_password_len(password) {
	  var strengthIndicator = document.getElementById('passwordStrength');
	  if (!validateStrongPassword(password)) {
			document.getElementById('len_pass_alert').style.color = '#DC3545';
			document.getElementById('len_pass_alert').innerHTML
			= '*Password must be at least 8 characters contain at least one uppercase,lowercase,number and special character';
			document.getElementById('create').disabled = true;
			document.getElementById('create').style.opacity = (0.4);
			
	  }else {
			document.getElementById('len_pass_alert').style.color = 'green';
			document.getElementById('len_pass_alert').innerHTML =
			'Strong password';
			document.getElementById('create').disabled = false;
			document.getElementById('create').style.opacity = (1);
		  }
		  validateForm();
	}
	


	function Username_valid() {
        var username = document.getElementById("username").value;			
        if(/\s/.test(username)) {
            document.getElementById('user_alert').style.color = '#DC3545';
            document.getElementById('user_alert').innerHTML
                = '☒ username cannot contain spaces.';
            document.getElementById('create').disabled = true;
            document.getElementById('create').style.opacity = (0.4);
        }else if(username == ""){
            document.getElementById('user_alert').style.color = '#DC3545';
            document.getElementById('user_alert').innerHTML
            = '☒ Please enter user name';
            document.getElementById('create').disabled = true;
            document.getElementById('create').style.opacity = (0.4);
        }
        else {
            document.getElementById('user_alert').style.color = 'green';
            document.getElementById('user_alert').innerHTML
                = ' User name is valid.';
            document.getElementById('create').disabled = false;
            document.getElementById('create').style.opacity = (1);
        }
        validateForm();
    }

	// function Email_valid() {
	// 	var email = document.getElementById("email").value;
	// 	var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	
	// 	if(!emailRegex.test(email)) {
	// 		document.getElementById('email_alert').style.color = '#DC3545';
	// 		document.getElementById('email_alert').innerHTML
	// 			= '☒ Please enter a valid email address.';
	// 		document.getElementById('create').disabled = true;
	// 		document.getElementById('create').style.opacity = (0.4);
	// 	}else {
	// 		document.getElementById('email_alert').style.color = 'green';
	// 		document.getElementById('email_alert').innerHTML
	// 			= 'Email is valid.';
	// 		document.getElementById('create').disabled = false;
	// 		document.getElementById('create').style.opacity = (1);
	// 	}
	// 	validateForm();
	// }
	

	function validateForm() {
		const len_pass_alert = document.getElementById('len_pass_alert');
		const wrong_pass_alert = document.getElementById('wrong_pass_alert');
		const user_alert = document.getElementById('user_alert');
		const email_alert = document.getElementById('email_alert');

		const isEmailValid = Email_valid();
		
		if (user_alert.innerHTML == 'name is valid.' && len_pass_alert.innerHTML == 'Strong password' && wrong_pass_alert.innerHTML == 'Password Matched' && email_alert =='') {
			document.getElementById('create').disabled = false;
			document.getElementById('create').style.opacity = (1);
		}
		else {
			document.getElementById('create').disabled = true;
            document.getElementById('create').style.opacity = (0.4);
		}
		return false; // Prevent form submission
	  }