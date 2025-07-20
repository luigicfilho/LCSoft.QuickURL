from app.services.auth_service import AuthService


def main():
    token = AuthService.create_admin_token()
    print(f"Admin Token:\n{token}")


if __name__ == "__main__":
    main()
