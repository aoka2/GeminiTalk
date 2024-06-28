function validateProfileForm() {
    var name = document.getElementById('name');
    var gender = document.getElementById('gender');
    var age = document.getElementById('age');
    var hobbies = document.getElementById('hobbies');
    var mbti = document.getElementById('mbti');
    var isValid = true;

    // Reset previous error states
    name.classList.remove('error');
    gender.classList.remove('error');
    age.classList.remove('error');
    hobbies.classList.remove('error');
    mbti.classList.remove('error');

    // Clear previous error messages
    name.placeholder = '';
    gender.placeholder = '';
    age.placeholder = '';
    hobbies.placeholder = '';
    mbti.placeholder = '';

    if (!isNaN(name.value)) {
        name.classList.add('error');
        name.value='';
        name.placeholder = '名前を入力してください';
        isValid = false;
    }
    if (!gender.value || (gender.value !== '男' && gender.value !== '女')) {
        gender.classList.add('error');
        gender.value='';
        gender.placeholder = '性別は「男」か「女」で入力してください';
        isValid = false;
    }
    if (!age.value || age.value < 18 || age.value > 100) {
        age.classList.add('error');
        age.value='';
        age.placeholder = '年齢を入力してください（18歳以上100歳以下）';
        isValid = false;
    }
    if (!isNaN(hobbies.value) || /[０-９]/.test(hobbies.value)) {
        hobbies.classList.add('error');
        hobbies.value='';
        hobbies.placeholder = '趣味を入力してください';
        isValid = false;
    }
    if (!isNaN(occupation.value) || /[０-９]/.test(occupation.value)) {
        occupation.classList.add('error');
        occupation.value='';
        occupation.placeholder = '職業を入力してください';
        isValid = false;
    }
    if (!isNaN(mbti.value) || /[０-９]/.test(mbti.value)) {
        mbti.classList.add('error');
        mbti.value='';
        mbti.placeholder = 'MBTIを入力してください';
        isValid = false;
    }

    return isValid;
}