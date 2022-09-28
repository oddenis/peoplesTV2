print('Hello!')
<form method="POST" id='formCrossOtpusk' actions="/createotpusk/" enctype="multipart/form-data" >
        {% csrf_token %}
{{ crossform.as_p }}
<button class="b_submit" type="submit" name="crossform" value="create_otpusk">Добавить сотрудника, с кем нельзя идти в отпуск вместе</button>
</form>