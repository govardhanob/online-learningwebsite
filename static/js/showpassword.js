function show() {
    var checkbox = document.getElementById('showPassword');
    var passwordField = document.getElementById('password');
    var passwordField1 = document.getElementById('password1');

    if (checkbox.checked) {
        if (passwordField1){
            passwordField1.type = "text";
        }
       
        passwordField.type = "text";
        
    } else {
        if (passwordField1){
            passwordField1.type = "password";
        }
        passwordField.type = "password";
        
    }
}
