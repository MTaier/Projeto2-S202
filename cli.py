from datetime import datetime
from services.hotel_service import HotelService


class CLIBase:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function, description):
        """Adiciona um comando ao CLI."""
        self.commands[name] = {"function": function, "description": description}

    def display_help(self):
        """Mostra os comandos disponíveis no CLI."""
        print("\nComandos disponíveis:")
        for command, details in self.commands.items():
            print(f"- {command}: {details['description']}")
        print()

    def run(self):
        """Executa o CLI."""
        print("\nBem-vindo ao sistema de gerenciamento de hotel!")
        print("Digite 'help' para ver os comandos disponíveis ou 'quit' para sair.")
        while True:
            command = input("\nDigite um comando: ").strip().lower()
            if command == "quit":
                print("Até logo!")
                break
            elif command == "help":
                self.display_help()
            elif command in self.commands:
                try:
                    self.commands[command]["function"]()
                except Exception as e:
                    print(f"Erro ao executar o comando: {e}")
            else:
                print("Comando inválido. Digite 'help' para ver os comandos disponíveis.")


class HotelCLI(CLIBase):
    def __init__(self, hotel_service):
        super().__init__()
        self.hotel_service = hotel_service
        self._register_commands()

    def _register_commands(self):
        """Registra os comandos do CLI."""
        self.add_command("create guest", self.create_guest, "Cria um novo hóspede.")
        self.add_command("create room", self.create_room, "Cria um novo quarto.")
        self.add_command("make reservation", self.make_reservation, "Faz uma reserva.")
        self.add_command("check-out", self.check_out, "Realiza o check-out de uma reserva.")
        self.add_command("get available rooms", self.get_available_rooms, "Exibe quartos disponíveis.")
        self.add_command("get guest reservations", self.get_guest_reservations, "Exibe reservas de um hóspede.")
        self.add_command("get active reservations", self.get_active_reservations, "Exibe reservas ativas.")
        self.add_command("get occupancy statistics", self.get_occupancy_statistics, "Exibe estatísticas de ocupação.")
        self.add_command("get revenue report", self.get_revenue_report, "Gera um relatório de receita.")
        self.add_command("get guest statistics", self.get_guest_statistics, "Exibe estatísticas de hóspedes.")
        self.add_command("get monthly occupancy", self.get_monthly_occupancy, "Exibe a ocupação mensal.")

    # Métodos de comandos
    def create_guest(self):
        name = input("Digite o nome do hóspede: ")
        email = input("Digite o email do hóspede: ")
        phone = input("Digite o telefone do hóspede: ")
        document = input("Digite o documento do hóspede: ")
        self.hotel_service.create_guest(name, email, phone, document)
        print("Hóspede criado com sucesso.")

    def create_room(self):
        number = input("Digite o número do quarto: ")
        room_type = input("Digite o tipo do quarto: ")
        price = float(input("Digite o preço do quarto: "))
        self.hotel_service.create_room(number, room_type, price)
        print("Quarto criado com sucesso.")

    def make_reservation(self):
        guest_id = input("Digite o ID do hóspede: ")
        room_number = input("Digite o número do quarto: ")
        check_in = input("Digite a data de check-in (YYYY-MM-DD): ")
        check_out = input("Digite a data de check-out (YYYY-MM-DD): ")
        self.hotel_service.make_reservation(guest_id, room_number, check_in, check_out)
        print("Reserva realizada com sucesso.")

    def check_out(self):
        reservation_id = input("Digite o ID da reserva: ")
        self.hotel_service.check_out(reservation_id)
        print("Check-out realizado com sucesso.")

    def get_available_rooms(self):
        rooms = self.hotel_service.get_available_rooms()
        print("\nQuartos disponíveis:")
        for room in rooms:
            print(f" - Número: {room['number']}, Tipo: {room['type']}, Preço: {room['price']}")

    def get_guest_reservations(self):
        guest_id = input("Digite o ID do hóspede: ")
        reservations = self.hotel_service.get_guest_reservations(guest_id)
        print("\nReservas do hóspede:")
        for res in reservations:
            print(f" - ID: {res['id']}, Quarto: {res['room_number']}, Check-in: {res['check_in']}, Check-out: {res['check_out']}")

    def get_active_reservations(self):
        reservations = self.hotel_service.get_active_reservations()
        print("\nReservas ativas:")
        for res in reservations:
            print(f" - ID: {res['id']}, Quarto: {res['room_number']}, Check-in: {res['check_in']}, Check-out: {res['check_out']}")

    def get_occupancy_statistics(self):
        stats = self.hotel_service.get_occupancy_statistics()
        print("\nEstatísticas de ocupação:")
        for stat in stats:
            print(f" - {stat['type']}: {stat['percentage']}% ocupado")

    def get_revenue_report(self):
        start_date = input("Digite a data inicial (YYYY-MM-DD): ")
        end_date = input("Digite a data final (YYYY-MM-DD): ")
        report = self.hotel_service.get_revenue_report(start_date, end_date)
        print("\nRelatório de receita:")
        for item in report:
            print(f" - Tipo: {item['type']}, Receita: {item['revenue']}")

    def get_guest_statistics(self):
        stats = self.hotel_service.get_guest_statistics()
        print("\nEstatísticas de hóspedes:")
        for stat in stats:
            print(f" - {stat['category']}: {stat['value']}")

    def get_monthly_occupancy(self):
        year = int(input("Digite o ano: "))
        month = int(input("Digite o mês: "))
        occupancy = self.hotel_service.get_monthly_occupancy(year, month)
        print(f"\nOcupação para {month}/{year}: {occupancy}%")


# Inicializando o CLI
if __name__ == "__main__":
    hotel_service = HotelService()
    hotel_cli = HotelCLI(hotel_service)
    hotel_cli.run()
