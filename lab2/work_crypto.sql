SELECT 
    user_id,
    email,
    pgp_sym_decrypt(encrypted_email, 'key') AS email_decrypted
FROM users 
LIMIT 5;



42503	april.schroeder@yahoo.com	april.schroeder@yahoo.com
42504	william.mendez@yahoo.com	william.mendez@yahoo.com
42507	jill.johnson@gmail.com	jill.johnson@gmail.com
42508	kayla.tucker@gmail.com	kayla.tucker@gmail.com
42509	ariel.shea@yahoo.com	ariel.shea@yahoo.com