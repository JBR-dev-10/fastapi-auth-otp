def test_update_profile(client):
    """Prueba de integración: Actualización exitosa del perfil de usuario."""
    client.post(
        "/auth/register",
        json={
            "email": "profile@example.com",
            "password": "Password123",
            "password_confirmation": "Password123",
            "full_name": "Original Name"
        }
    )
    
    login_res = client.post(
        "/auth/login",
        json={
            "email": "profile@example.com",
            "password": "Password123"
        }
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Actualizar perfil
    update_res = client.put(
        "/users/profile",
        headers=headers,
        json={"full_name": "Updated Name"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["full_name"] == "Updated Name"