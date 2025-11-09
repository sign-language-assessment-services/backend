# TODO: -- PLAN --
#       1. Von app/rest (requests, responses und routers) Funktionalität bereitstellen für
#          CRUD-Methoden, die dann vom Service-Layer aufgegriffen wird (Fokus auf create, falls
#          Zeit und Muse, gerne auch upsert-Funktionalität).
#       2. Alle Entitäten sollten so gut es geht, ohne Abhänigkeiten kreiert werden können. Z. B.
#          sollte es möglich sein, eine leere Exercise anzulegen, ohne bereits die Abhängigkeiten
#          (Frage + Multiple Choice) zu kennen.
#       3. Im Service-Layer Funktionalität von den Endpunkten (Business-Logik) ausführen und
#          die entsprechenden repositories ansprechen. Darauf achten, dass alles konsistent ist,
#          also z. B. Business-Logik tatsächlich im Service-Layer ist. Dafür benötigt es diverse
#          refactorings, z. B. in Endpunkten, wo bereits Logik gemacht wird. (vgl. add vs create)
#       4. Filtermöglichkeiten sollten existieren, damit man u. a. einfach exercise submissions
#          von bestimmten usern filtern kann usw.
#       5. Detaillierte Logs einbauen (lifespan schluckt logs -> beheben)
#       6. Endpunkte dürfen gerne besser dokumentiert sein. Dafür bietet FastAPI einige Möglichkeiten,
#          u. a. response_model in den Pfadangaben oder erweiterte Dokumentation
#       7. Status-Codes, die zurückgegeben werden überprüfen (auch hinsichtlich async, created vs ok)
#          Fehlerfälle bedenken und API richtige Fehlercodes zurückgeben lassen
#       8. Middleware oder Dekorator für Rollen-Checks anstatt überall if-Abfragen.
#       9. Performance-Tests, Integrations-Tests, e2e-Tests
#      10. Architektur-Dokumentation updaten
#      11. Async generell überprüfen, z. B. hat auch postgres einen async Treiber
#      12. Replace UUID with ULID: https://github.com/mdipierro/ulid
