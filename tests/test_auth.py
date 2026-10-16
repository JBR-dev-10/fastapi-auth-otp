def test_register_user(client):
    """Prueba unitaria / integración: Registro exitoso de usuario."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePassword123",
            "password_confirmation": "SecurePassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

def test_register_password_mismatch(client):
    """Prueba unitaria: Falla cuando las contraseñas no coinciden."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test2@example.com",
            "password": "SecurePassword123",
            "password_confirmation": "DifferentPassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 422

def test_login_and_logout(client):
    """Prueba de integración: Inicio de sesión y cierre de sesión con revocación de token."""
    # Registrar
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "Password123",
            "password_confirmation": "Password123",
            "full_name": "Login User"
        }
    )
    
    # Login
    login_res = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123"
        }
    )
    assert login_res.status_code == 200
    tokens = login_res.json()
    assert "access_token" in tokens
    
    # Probar perfil con token
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    profile_res = client.get("/users/profile", headers=headers)
    assert profile_res.status_code == 200
    assert profile_res.json()["email"] == "login@example.com"
    
    # Logout
    logout_res = client.post("/auth/logout", headers=headers)
    assert logout_res.status_code == 200
    
    # Intentar usar el token revocado debe fallar
    profile_after_logout = client.get("/users/profile", headers=headers)
    assert profile_after_logout.status_code == 401