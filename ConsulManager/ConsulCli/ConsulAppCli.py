import curses
from datetime import date
from ConsulManager.ConsulCli.newConsultaApp import newConsultaApp
from ConsulManager.AirTable.Utilities.Fechas import get_valid_date, get_week
from ConsulManager.AirTable.reportesAir.ReportAir import ReportManagerAir
from ConsulManager.AirTable.Consultas.ConsultasManagerAir import ConsultasManagerAir
from ConsulManager.AirTable.Cobros.CobrosManagerAir import CobrosManagerAir
from ConsulManager.AirTable.PagosDentistas.PagosDentistas import PagosDentistasAir
from ConsulManager.AirTable.Tratamientos.TratamientosManagerAir import TratamientoManagerAir
from ConsulManager.Logger import logger as log
import re


if __name__ == '__main__':
    # curses.wrapper(main)
    # app = consulApp(state_machine=NEW_CONSULTA_ST, init_state=GET_CONSULTA_DATE_ST, pacientes_table=True)
    app = newConsultaApp(debug_mode=True)
    curses.wrapper(app.run)
    consulta_list = app.get_data()
    new_report = ReportManagerAir()

    log.info("Start to generate consultas ...")

    

    consulta_index = 0
    for consulta in consulta_list:
        log.info(f"Generating Consulta index:{consulta_index}")

        # get week id
        valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
        (day, month, year) = valid_date.match(string=consulta['fecha']).groups()
        valid_week = get_week(year=int(year), month=int(month), day=int(day))
        week_id = new_report.get_week_record(week=valid_week)
        log.info(f"Week Id: {week_id}")

        # tratamientos
        print(consulta)
        if consulta["tratatamiento_id"] is not None:
            tratamientos_id_list = []

            # todo es solo una lista con el id hay que modificarlo

            # if type(consulta["tratatamiento_id"]) != list:
            for tratamiento in consulta["tratatamiento_id"]:
                print(f"{tratamiento=}")
                if tratamiento.get("tratamiento_id_list") is None:
                    tratamiento["tratamiento"] = [tratamiento["tratamiento"]]
                    print(tratamiento)

                    # date
                    valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
                    (day, month, year) = valid_date.match(string=tratamiento['fecha']).groups()
                    tratamiento['fecha'] = get_valid_date(year=int(year), month=int(month), day=int(day))



                    tratamientos_table = TratamientoManagerAir()
                    record = tratamientos_table.create_tratamiento(**tratamiento)
                    log.info(f"    - generating new Tratamiento id: {record['id']}")
                    tratamientos_id_list.append(record['id'])
                else:
                    tratamientos_id_list.append(tratamiento["tratamiento_id_list"])
            consulta['tratatamiento_id'] = tratamientos_id_list


        # cobros
        if consulta["cobros"] is not None:
            cobros_id_list = []
            for cobro in consulta["cobros"]:
                # date
                valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
                (day, month, year) = valid_date.match(string=cobro['fecha']).groups()
                cobro['fecha'] = get_valid_date(year=int(year), month=int(month), day=int(day))

                # log.info(f"   - generating new COBRO {cobro}")
                cobros_table = CobrosManagerAir()
                cobro["semana"] = [week_id]
                record = cobros_table.create_cobro(**cobro)
                log.info(f"    - generating new COBRO id: {record['id']}")
                cobros_id_list.append(record['id'])
            consulta['cobros'] = cobros_id_list

        # pagos
        # print(consulta)
        if consulta["pagos_dentistas"] is not None:
            pagos_id_list = []
            for pago in consulta["pagos_dentistas"]:
                # date
                valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
                (day, month, year) = valid_date.match(string=pago['fecha']).groups()
                pago['fecha'] = get_valid_date(year=int(year), month=int(month), day=int(day))
                pago['semana'] = [week_id]

                pagos_table = PagosDentistasAir()
                record = pagos_table.create_pago(**pago)
                log.info(f"    - generating new Pago id: {record['id']}")
                pagos_id_list.append(record['id'])
            consulta['pagos_dentistas'] = pagos_id_list

        

        consulta["semana"] = [week_id]
        consulta["fecha"] = get_valid_date(year=int(year), month=int(month), day=int(day))
        consulta['paciente'] = [consulta['paciente']]

        log.info(f"    date:{consulta['fecha']} week:{valid_week} week_id:{week_id}")

        print(consulta)
        consultas_table = ConsultasManagerAir()
        consultas_table.create_consulta(**consulta)


        consulta_index += 1
        