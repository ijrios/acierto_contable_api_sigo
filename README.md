
**API´S SIIGO ACIERTO CONTABLE**

**Manual técnico**

# Contenido
[1.	Introducción](#_toc178152708)

[2.	Proyecto](#_toc178152709)

[3.	Objetivo general](#_toc178152710)

[4.	Objetivos específicos](#_toc178152711)

[5.	Como interactúa el usuario](#_toc178152712)

[6.	Gestión de Compañías, Usuarios y Roles](#_toc178152713)

[7.	Explicación pseudocódigo por modulo](#_toc178152717)

[MÓDULO DE USUARIOS](#_toc178152718)

[MÓDULO DE COMPAÑÍA](#_toc178152719)

[MÓDULO DE REPORTES](#_toc178152720)

[8.	Requisitos](#_toc178152721)

[8.1	Versiones de las librerías y programas utilizados](#_toc178152722)

[8.2	Requisitos no funcionales](#_toc178152723)

[8.3	Requisitos del servidor, de las plataformas, de las credenciales](#_toc178152724)

[8.4	Frecuencia de ejecución de la solución](#_toc178152725)


1. # <a name="_toc178152708"></a>**Introducción**

**APPI’S SIIGO - ACIERTO CONTABLE** es una solución creada para mejorar y automatizar la gestión contable a través de su integración con el software Siigo. Este manual tiene el propósito de guiar a los usuarios en la utilización de las APIs desarrolladas para realizar consultas críticas sobre la contabilidad de la empresa. Adicionalmente, el sistema cuenta con un enfoque robusto en la seguridad de los datos, garantizando que el acceso a la información esté restringido según roles asignados, lo que asegura que solo usuarios autorizados puedan interactuar con datos específicos según sus permisos.

1. # <a name="_toc178152709"></a>**Proyecto**
APPI´S SIIGO- ACIERTO CONTABLE
#
1. # <a name="_toc178152710"></a>**Objetivo general**
Proveer una guía para el uso de las APIs de Siigo integradas en ACIERTO CONTABLE, facilitando la gestión de la información contable, empresarial y de usuarios a través de los módulos de reportes, compañía y usuarios y roles, optimizando así la administración y toma de decisiones dentro de la organización.

1. # <a name="_toc178152711"></a>**Objetivos específicos** 

- **Implementar consultas contables automatizadas:** Emplear las APIs del módulo de reportes para consultar de manera eficiente el Plan Único de Cuentas (PUC), movimientos contables por terceros, ventas por cliente y producto, reporte de comprobantes detallados, cuentas por pagar. Este objetivo busca optimizar la generación de reportes contables y el acceso rápido a la información financiera.
- **Facilitar el acceso a la información de la compañía:** Emplear las APIs del módulo de compañía para consultar y actualizar los datos generales de la empresa, garantizando que la información clave esté siempre al día y disponible para su uso en procesos contables.
- **Gestionar roles y usuarios con seguridad:** Emplear las APIs del módulo de usuarios y roles para asignar permisos y controlar el acceso a la información dentro del sistema. Este objetivo asegura que solo usuarios autorizados puedan acceder a los datos sensibles y realizar modificaciones en la plataforma.

1. # <a name="_toc178152712"></a>**Como interactúa el usuario** 
Los usuarios interactúan con el sistema a través de las APIs proporcionadas por el backend. Para registrar información o realizar consultas, los usuarios deben consumir estas APIs desde sus aplicaciones frontend, herramientas como Power BI, o alguna aplicación que requiera estor reportes financieros de la empresa. El backend gestionará y procesará las solicitudes, devolviendo los datos necesarios para la generación de reportes y análisis. El sistema se asegura de que las APIs proporcionen la información correcta y relevante de acuerdo con los permisos y roles asignados a cada usuario, garantizando así un acceso seguro y eficiente a los datos.


1. # <a name="_toc178152713"></a>**Gestión de Compañías, Usuarios y Roles**

**El primer paso consiste en crear la compañía. Una vez creada, es necesario listar las compañías para obtener el ID correspondiente. Con este ID, se asignan las credenciales a la compañía y se procede a crear el usuario. Se ha implementado una funcionalidad adicional que, al crear una nueva compañía, genera automáticamente un usuario administrador por defecto. Este administrador está preconfigurado con un rol que les otorga acceso completo a todas las consultas relacionadas con la empresa. Si se desea crear manualmente usuarios no administradores, es necesario asignarles roles específicos. Existen 11 roles definidos en el módulo de roles. Primero, se deben listar los roles para obtener su ID. Luego, con el ID del rol y el ID de la compañía, se puede crear el nuevo usuario.**
#
1. # <a name="_toc178152717"></a>**Explicación pseudocódigo por modulo**
#
# <a name="_toc127177898"></a><a name="_toc178152718"></a>**MÓDULO DE USUARIOS:**
*El modelo de usuarios gestiona la información relacionada con los usuarios dentro del sistema. Almacena datos como nombre, correo electrónico, contraseña encriptada, roles, y permisos. Este modelo es fundamental para la autenticación y autorización, permitiendo el control de acceso a diferentes funcionalidades de la aplicación. Además, puede incluir atributos adicionales como el estado de la cuenta, fechas de creación y actualización, y relaciones con otros modelos para definir permisos específicos o asociaciones con grupos.*

- **POST - *LOGIN***

<http://174.138.176.171:82/login/>

Este Api permite a los usuarios autenticarse en el sistema. El usuario debe proporcionar su nombre de usuario y contraseña, y si las credenciales son correctas, se generará un token de autenticación o sesión válida para acceder a las diferentes funcionalidades protegidas del sistema. Este token se suele enviar en las solicitudes posteriores para verificar que el usuario está autorizado.

**Ejemplo de solicitud.**

{

`    `"username":"admin",

`    `"password":"admin"

}

- **GET - *LIST-USERS (Superuser)***

<http://174.138.176.171:82/users/user-list/>

Este Api devuelve una lista de todos los usuarios registrados en el sistema. Es una consulta de solo lectura que puede ser utilizada por superusuarios para revisar quiénes están registrados y poder obtener su ID para realizar algunas peticiones.


- **GET - *USER-LIST-BY-COMPANY***

<http://174.138.176.171:82/users/user-list/>

Este Api devuelve una lista de todos los usuarios registrados en el sistema por compañía. Es una consulta de solo lectura que puede ser utilizada por el administrador por defecto de cada compañía, para revisar quiénes están registrados y poder obtener su ID para realizar algunas peticiones.

- **POST - *CREATE-USER***

<http://174.138.176.171:82/users/register/>

Este Api permite crear un nuevo usuario en el sistema. Se deben enviar los datos del usuario, como el nombre, apellido, empresa asociada, correo electrónico, nombre de usuario, contraseña y rol. Este método es utilizado por administradores para gestionar la creación de nuevas cuentas de usuario.

**Ejemplo de solicitud.**

{

`    `"first\_name": "Diego Alexandro",

`    `"last\_name": "Rojas Giraldo",

`    `"company": 1,

`    `"email": "diego2@gmail.com",

`    `"username": "diego1",

`    `"password": "1234",

`    `"document": "12345689",

`     `"rol": 7

}

- **PUT - *EDIT-USER***

<http://174.138.176.171:82/users/user/1/>

Este Api permite editar la información de un usuario existente en el sistema. La URL incluye el ID del usuario que se desea modificar, y en el cuerpo de la solicitud se deben enviar los campos que se desean actualizar, como la compañía, el correo o el rol. Solo los usuarios con permisos de administración pueden realizar esta operación.

`      `**Ejemplo de solicitud.**

{

`    `"company":1

}
#
#
#
#
- **GET: *ACTIVATE - DEACTIVATE - USER***

<http://174.138.176.171:82/users/user/11/activate/>

Esta API es utilizada para cambiar el estado de activación de un usuario y así gestionar su disponibilidad en el sistema. Se debe listar primero los usuarios para así saber su ID que debe ser puesto en la URL de la petición. Esta funcionalidad solo está permitida para el usuario con el rol de administrador. 

- **GET: *LOGOUT***

<http://174.138.176.171:82/logout/?access_token=9268254a2dbe8207c5166abf37516b24a24b2066>

Esta API es utilizada para cerrar sesión. Se debe obtener de los headers el token para poder agregarlo a la URL del API. Esta funcionalidad solo está permitida para el usuario con el rol de administrador. 
#
# <a name="_toc178152719"></a>**MÓDULO DE COMPAÑÍA**
#
*Los usuarios interactúan con el modelo de compañía a través de una serie de APIs que permiten gestionar la información de las compañías y sus credenciales. Esto incluye listar todas las compañías disponibles, crear nuevas compañías con los datos necesarios, actualizar información de compañías existentes, y activar o desactivar compañías según sea necesario. Además, los usuarios pueden gestionar las credenciales asociadas a cada compañía, ya sea creando nuevas o actualizando las existentes. El modelo de compañías gestiona datos básicos como el NIT (Número de Identificación Tributaria) y la razón social, permitiendo identificar y registrar cada empresa de manera única y estableciendo relaciones con otros módulos del sistema.*

- **POST - CREATE\_COMPANIE**

<http://174.138.176.171:82/users/company-create/>

Los usuarios autorizados pueden agregar nuevas compañías al sistema utilizando este API para la creación de compañías. Esta funcionalidad solo está permitida para el usuario con el rol de superusuario. Al crear la compañía, se crea un usuario administrador por defecto, este usuario viene con todos los roles habilitados. Esta petición requiere que se envíe esta información específica sobre la compañía en formato JSON:

- NIT: El Número de un identificador único para cada empresa.
- Nombre de la Empresa.

**Ejemplo de solicitud.**

{

`    `"nit":"124981241",

`    `"business\_name": "Empresa de Prueba"

}

- **GET – LIST-COMPANIES**

<http://174.138.176.171:82/companies/company-list/>

Este Api obtiene una lista completa de todas las compañías registradas, permitiendo la visualización de sus datos básicos. Esta funcionalidad solo está permitida para el usuario con el rol de administrador.

- **GET: COMPANY-UPDATE**

<http://174.138.176.171:82/companies/company-update/15/>

Esta API es utilizada para modificar los datos de una compañía existente para reflejar cambios o correcciones. Se debe listar primero la compañía para así saber su ID que debe ser puesto en la URL de la petición. Esta funcionalidad solo está permitida para el usuario con el rol de administrador. Se debe enviar en la solicitud estos datos en formato JSON:

**Ejemplo de solicitud.**

{

`    `"business\_name": "Bancolombia"

}

- **POST: COMPANY-ACTIVE**

<http://174.138.176.171:82/companies/company-activate/15/activate/>

Esta API es utilizada para cambiar el estado de activación de una compañía y así gestionar su disponibilidad en el sistema. Se debe listar primero la compañía para así saber su ID que debe ser puesto en la URL de la petición. Esta funcionalidad solo está permitida para el usuario con el rol de administrador. 

- **POST: CREDENTIAL-CREATE**

<http://174.138.176.171:82/users/rol-list/>

Esta API es utilizada para almacenar las credenciales para una compañía, incluyendo información de acceso y permisos. Estas credenciales son necesarias para la conexión que se hace con SIIGO, el cual nos permite consumir las APIs con información financiera de la compañía. Esta funcionalidad solo está permitida para el usuario con el rol de administrador.

**Ejemplo de solicitud.**

{

`    `"user\_siigo":"info@aciertocontable.com",

`    `"secret\_key\_siigo":"NDA0Mzc2NTAtNzQ2MS00ZjQxLTk2MTQtZWE5YzVhOWYxYTdkOjN7NTl+Y2J5N1I=",

`    `"company": 1

}

- **PUT:** **CREDENTIAL-UPDATE**

<http://174.138.176.171:82/companies/credential-update/4/>

Esta API es utilizada para actualizar las credenciales para una compañía, incluyendo información de acceso y permisos. Se debe listar primero la compañía para así saber su ID que debe ser puesto en la URL de la petición. Estas credenciales son necesarias para la conexión que se hace con SIIGO, el cual nos permite consumir las APIs con información financiera de la compañía. Esta funcionalidad solo está permitida para el usuario con el rol de administrador.

**Ejemplo de solicitud.**

{

`    `"user\_siigo":"info@aciertocontable.com",

`    `"secret\_key\_siigo":"cualquier\_secrect\_key\_nueva\_por actualizar”

}

# <a name="_toc178152720"></a>**MÓDULO DE REPORTES:**
#
*El módulo de reportes en ACIERTO CONTABLE es fundamental para la aplicación, ofreciendo acceso a APIs que permiten extraer y analizar datos contables esenciales. A través de estas APIs, los usuarios pueden obtener informes detallados que cubren una variedad de áreas financieras. Este módulo facilita la generación de informes estructurados que son cruciales para el análisis financiero y la toma de decisiones en la empresa. Total de consultas: PUC, Balance general, Balance general Excel, Movimiento contables por terceros, movimientos contables por terceros Excel, Reporte de ventas por cliente por producto resumido, Reporte de ventas por cliente por producto detallado, Cartera general detallada por cliente, Cartera general por cliente, Cuentas por pagar detallada por proveedor, Reporte de comprobantes detallados*

- **GET: PUC**

<http://174.138.176.171:82/reports/puc/>

El Plan Único de Cuentas (PUC), el cual es un catálogo de cuentas contables que estandariza las cuentas financieras que una empresa debe utilizar para registrar sus transacciones. 

Campos: 

•	Código: Identificación de la cuenta contable.

•	Cuenta Contable: Nombre de la cuenta contable.

•	Clase: Clasificación general de la cuenta.

•	Grupo: Nivel jerárquico

•	Tipo y subtipo: Nivel jerárquico.


- **GET: GENERAL-BALANCE (Balance general de la empresa)**

<http://174.138.176.171:82/reports/general-balance/>

Esta API devuelve el balance general de la empresa, que es un informe financiero que proporciona un resumen de los activos, pasivos y el patrimonio neto de la empresa en un momento específico. El balance general refleja la posición financiera de la empresa y ayuda a evaluar su estabilidad económica y solvencia.

*También se genera un api adicional que devuelve una url para descargar esta información en Excel.*

***Excel**: [http://174.138.176.171:82/reports/general-balance-excel/*](http://174.138.176.171:82/reports/general-balance-excel/)*

Campos: 

- Nivel
- Trasaccional
- Codigo\_cuenta\_contable
- Nombre\_cuenta\_contable
- Saldo\_inicial
- Movimiento\_debito
- Movimiento\_credito
- Saldo\_final         

- **GET: REPORT-BY-THIRDPARTY-JSON (Movimiento contable por terceros)**

<http://174.138.176.171:82/reports/report-by-thirdparty-json/>

Esta API devuelve los movimientos contables asociados a un tercero específico (cliente, proveedor, empleado, etc.). Los movimientos contables son registros de transacciones financieras que afectan las cuentas del PUC.

*También se genera un api adicional que devuelve una url para descargar esta información en Excel.*

***Excel:** [http://174.138.176.171:82/reports/report-by-thirdparty/*](http://174.138.176.171:82/reports/report-by-thirdparty/)*

Campos: 

- Nivel
- Trasaccional
- Codigo\_cuenta\_contable
- Nombre\_cuenta\_contable
- Identificación\_tercero
- Nombre\_tercero
- Saldo\_inicial
- Movimiento\_debito
- Movimiento\_credito
- Saldo\_final         

- **GET: SALES (Reporte de ventas por cliente por producto)**

[http://174.138.176.171:82/reports/sales/1/](http://174.138.176.171:82/reports/sales/1/1) (Mes actual)

<http://174.138.176.171:82/reports/sales/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/sales/3/>  (Semestre actual)

Esta API devuelve un informe de las ventas realizadas, agrupadas por cliente y desglosadas por producto, incluye sus impuestos y cantidades vendidas, de allí se puede obtener valores por unidad para informes. Contine los siguientes campos, mismos que se muestran en la plataforma de SIIGO (solo le agregamos fecha): 

- ID del cliente: NIT del cliente
- Nombre cliente
- Código de producto
- Nombre producto
- Cantidad\_vendida
- Fecha de venta
- Subtotal: valor sin impuestos
- Impuesto retención: Impuesto del 0.11
- Impuesto de cargo: Impuesto del 0.19
- Total

- ` `**GET: SALES-MORE (Reporte de ventas por cliente por producto con todos los detalles)**

<http://174.138.176.171:82/reports/sales-more/1/>  (Mes actual)

<http://174.138.176.171:82/reports/sales-more/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/sales-more/3/>  (Semestre actual)

Esta API devuelve un informe de las ventas realizadas, agrupadas por cliente y desglosadas por productos y con todos sus detalles.

- **GET: SALES-CUSTOMER (Reporte de ventas totales por clientes, posible indicador de ventas)**

<http://174.138.176.171:82/reports/sales-customer/1/>  (Mes actual)

<http://174.138.176.171:82/reports/sales-customer/2/>  (Trimestre actual)

[http://174.138.176.171:82/reports/sales-customer/3/](http://174.138.176.171:82/reports/sales-customer/3/3)  (Semestre actual)

Esta API devuelve un informe de las ventas totales realizadas, agrupadas por cliente. 




- **GET: TESSERA\_TOTAL (Cartera general detallada por cliente)**

<http://174.138.176.171:82/reports/monetae-duo/1/>  (Mes actual)

<http://174.138.176.171:82/reports/monetae-duo/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/monetae-duo/3/>  (Semestre actual)

Esta API devuelve un informe detallado de la cartera (deudas pendientes) de cada cliente de manera general, devuelve la misma información de la página de SIIGO: 


- **GET: TESSERA\_CLIENT (Cuentas por pagar cliente, cartera detallada por cliente)**

<http://174.138.176.171:82/reports/monetae-duo/1/>  (Mes actual)

<http://174.138.176.171:82/reports/monetae-duo/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/monetae-duo/3/>  (Semestre actual)

Esta API devuelve un informe detallado de la cartera individual por cada cliente, mostrando las cuentas por pagar por cada uno con sus respectivos días de vencimiento de la deuda, es la misma información mostrada en la página de SIIGO, esta información sale cuando se presiona el enlace de la cartera del cliente:


- **GET: ACCOUNTS-PAYABLE (Cuentas por pagar detallada por proveedor, datos importantes tal como en la plataforma SIIGO)**

<http://174.138.176.171:82/reports/accounts-payable/1/>  (Mes actual)

<http://174.138.176.171:82/reports/accounts-payable/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/accounts-payable/3/>  (Semestre actual)

Esta API devuelve un informe detallado de la cartera (deudas pendientes) de cada cliente. Contiene los siguientes campos:

- Identificación del cliente
- Nombre del proveedor
- Deuda por pagar
- Valor anticipos
- Saldo proveedor
- Valor vencido

- **GET: ACCOUNTS-PAYABLE (Cuentas por pagar general por proveedor, datos completos)**

<http://174.138.176.171:82/reports/accounts-payable-general/1/>  (Mes actual)

<http://174.138.176.171:82/reports/accounts-payable-general/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/accounts-payable-general/3/>  (Semestre actual)

Esta API devuelve un informe detallado de la cartera (deudas pendientes) de cada cliente.

- **GET: JOURNALS (Reporte de comprobantes detallados, datos importantes)**

<http://174.138.176.171:82/reports/journals/1/>  (Mes actual)

<http://174.138.176.171:82/reports/journals/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/journals/3/>  (Semestre actual)

Esta API devuelve un informe detallado de todos los comprobantes de contabilidad, que son documentos que respaldan las transacciones financieras, se obtienen los datos más importantes:

- Fecha
- Código cuenta contable
- Movimiento (crédito o débito)
- Fecha
- Id del cliente
- Nombre del cliente
- Descripción 
- Valor del comprobante

- **GET: JOURNALS (Reporte de comprobantes detallados, datos completos)**

<http://174.138.176.171:82/reports/journals-general/>1/

<http://174.138.176.171:82/reports/journals-general/>2/

<http://174.138.176.171:82/reports/journals-general/>3/


Esta API devuelve un informe detallado de todos los comprobantes con sus datos completos.


- **GET: CUSTOMERS (Clientes y proveedores)**

<http://174.138.176.171:82/reports/customer/>

Esta API devuelve un informe detallado de todos los clientes y proveedores de la empresa, devuelve un JSON con toda la información detallada de cada cliente, números de contacto e información importante personal.

- **GET: CUSTOMERS\_NEW (Clientes nuevos de cada mes, semestre o trimestre, para crear indicador)**

<http://174.138.176.171:82/reports/customer-new/1/>  (Mes actual)

<http://174.138.176.171:82/reports/customer-new/2/>  (Trimestre actual)

<http://174.138.176.171:82/reports/customer-new/3/>  (Semestre actual)


Esta API devuelve un informe detallado de todos los clientes y proveedores de la empresa, devuelve un JSON con toda la información detallada de cada cliente, números de contacto e información importante personal.


- **GET: PRODUCTS** 

<http://174.138.176.171:82/reports/products/>

Esta API devuelve un informe detallado de todos los productos registrados y ofrecidos por la empresa, devuelve un JSON con toda la información detallada de cada producto.


**MÓDULO DE ROLES:**

*Este módulo de roles es un componente importante en aplicaciones que requieren privacidad y seguridad de los datos, los roles que se asignan permiten el acceso a las 8 consultas y en caso contrario, lo deniegan. Un usuario puede contener varios roles, se pueden crear tantos roles como sea necesario. Para ello se construyen dos principales API, que se encargan de crearlos o actualizarlos. Luego de crear el rol, se debe ejecutar la consulta de edición de usuarios y en el campo "Role" del JSON de salida, ingresar el id del rol correspondiente, este id se puede encontrar ejecutando el api que muestra la lista de los roles con su información (rol-list).*

- **POST: CREATE\_ROLES**

<http://174.138.176.171:82/users/create_roles/>

Esta API se utiliza para crear nuevos roles. Cuando un nuevo rol es creado, se definen los permisos asociados a él, permitiendo o restringiendo el acceso a las diferentes consultas según sea necesario. Para su creación se debe enviar la siguiente información en formato JSON:

- Nombre del rol
- Descripción detallada del rol y funciones permitidas
- Permisos que tendrá el empleado, aquí se debe ingresar una lista que contiene los roles (solo deben ser números y del 1 al 8, de lo contrario saldrá mala la consulta), ejemplo: [ 1,2,3].

**Ejemplo de solicitud.**

{

`    `"name": "Asesor",

`    `"description": "Tiene solo permiso de ventas y cartera general",

`    `"permissions":[3,4]

}

**Roles creados** (pueden ser modificados por el superusuario en la siguiente petición):

- PUC: **1**
- Movimientos contables terceros: **2**
- Ventas por producto por cliente: **3**
- Cartera cliente: **4**
- Cuentas por pagar: **5**
- Comprobantes detallados: **6**
- Clientes y productos: **7 y 8**
- Usuarios (creación, actualización, ect): **9**
- Roles (creación, actualización, ect): **10** 
- Compañía (creación, actualización, ect): **11**


- **POST: UPDATE\_ROLES**

<http://174.138.176.171:82/users/update_roles/2/>

Esta API se encarga de actualizar roles existentes. A través de este método, se pueden modificar los permisos de un rol previamente creado, ajustando los accesos de acuerdo con las nuevas necesidades de la aplicación.

**Para su creación se debe enviar la siguiente información en formato JSON:**

- Permisos que tendrá el empleado, aquí se debe ingresar una lista que contiene los roles (solo deben ser números y del 1 al 8, de lo contrario saldrá mala la consulta), ejemplo: [ 1,2,3].
- En el api vemos **users/update/2/**, el número 2 es el id del empleado al que vamos a modificar o agregar permisos, es necesario listar los usuarios primero para así saber su id, se pueden listar los usuarios con el api ya mencionada que muestra una lista de todos los usuarios.

**Ejemplo de solicitud.**

{

`    `"permissions":[2,3,4]

}

- **GET: ROL-LIST (Superusuario)**

<http://174.138.176.171:82/users/rol-list/>

Esta API es utilizada para recuperar una lista completa de todos los roles disponibles en el sistema. A través de esta funcionalidad, los superuruarios y otros usuarios con los permisos adecuados pueden visualizar todos los roles existentes, junto con sus permisos asociados. Esto es útil para auditar y gestionar los roles de manera eficiente, asegurando que los usuarios tengan los permisos correctos y que se mantenga la integridad de las políticas de acceso en la aplicación.

- **GET: ROLE-LIST-BY-COMPANY**

`      `<http://174.138.176.171:82/users/rol-list-company/1/>

Esta API es utilizada para recuperar una lista completa de todos los roles disponibles en el sistema por cada empresa, y solo puede ser vista por el usuario administrador de la empresa en específico.


1. # <a name="_toc178152721"></a>**Requisitos**
#
1. # <a name="_toc178152722"></a>**Versiones de las librerías y programas utilizados**
   #
- **Python 3.12:** La versión de Python utilizada para el desarrollo del backend, y se recomienda instalarla desde la tienda de Microsoft Store.
- **Django Rest Framework:** Framework utilizado para construir APIs RESTful en Django. Versión utilizada: 3.14.0.
- **Pandas Python**: Librería de análisis de datos que facilita la manipulación de datos en estructuras como DataFrames. Versión utilizada: 2.2.2.
- **Requests Python:** Librería simple para hacer solicitudes HTTP. Versión utilizada: 2.32.3.

`                       `**Librerías adicionales utilizadas en el proyecto:**

Estas librerías están en el archivo (requeriments.txt) en la raíz del proyecto, y pueden ser instaladas fácilmente con el comando:

*pip install -r requirements.txt*

- **asgiref==3.8.1:** Librería para la implementación de ASGI, usada en servidores de aplicaciones y websockets.
- **certifi==2024.7.4:** Librería que proporciona certificados de raíz para solicitudes HTTP seguras.
- **charset-normalizer==3.3.2:** Biblioteca que se utiliza para la detección y normalización de codificaciones de caracteres.
- **Django==5.0.7:** Framework web de alto nivel que fomenta un desarrollo rápido y limpio en Python.
- **django-cors-headers==4.4.0:** Manejador de CORS en Django para permitir solicitudes entre dominios.
- **et-xmlfile==1.1.0:** Librería para generar XML utilizados, por ejemplo, en archivos de Excel.
- **idna==3.8:** Implementación del estándar de codificación IDNA (Internationalized Domain Names).
- **numpy==2.1.0:** Paquete de Python para computación numérica de alto rendimiento.
- **openpyxl==3.1.5:** Librería para trabajar con archivos Excel en formato .xlsx.

- **pillow==10.4.0:** Biblioteca de imágenes de Python que añade capacidades de procesamiento de imágenes.
- **psycopg2==2.9.9:** Adaptador de base de datos PostgreSQL para Python.
- **python-dateutil==2.9.0.post0:** Extensiones del módulo datetime para manejo de fechas.
- **python-dotenv==1.0.1:** Carga variables de entorno desde un archivo .env.
- pytz==2024.1: Biblioteca para trabajar con zonas horarias y tiempos globales.
- **six==1.16.0:** Ayuda a escribir código compatible con Python 2 y 3.
- **sqlparse==0.5.1:** Librería para el análisis y formateo de sentencias SQL.
- **tzdata==2024.1:** Base de datos de zonas horarias.
- **urllib3==2.2.2:** Potente cliente HTTP en Python para realizar solicitudes HTTP con múltiples funcionalidades avanzadas
#
1. # <a name="_toc178152723"></a>**Requisitos no funcionales**
   #
**Seguridad:** El sistema debe garantizar la seguridad de la información ingresada y de los procesos que se llevan a cabo en el sistema.

**Accesibilidad**: El sistema debe ser accesible a todos los usuarios autorizados en todo momento y desde cualquier lugar con acceso a Internet.

**Confiabilidad:** El sistema debe ser confiable y estar disponible en todo momento, garantizando una disponibilidad adecuada para los usuarios.

**Usabilidad**: El sistema debe ser fácil de usar para todos los usuarios, incluyendo una interfaz intuitiva y una navegación clara.

**Performance:** El sistema debe ser capaz de manejar una gran cantidad de información y procesos en tiempo real sin tener retrasos o interrupciones.

**Integridad de datos:** El sistema debe garantizar la integridad de los datos ingresados y de los procesos que se llevan a cabo en el sistema.

**Responsabilidad:** El sistema debe asignar responsabilidades claras a los diferentes usuarios y garantizar que los procesos se lleven a cabo de manera eficiente.

**Monitoreo y control:** El sistema debe ser capaz de monitorear y controlar los procesos y alertar a los usuarios cuando sea necesario.

1. # <a name="_toc178152724"></a>**Requisitos del servidor, de las plataformas, de las credenciales**
Para el correcto funcionamiento del sistema, es fundamental que cada usuario esté asociado a una compañía. Esta compañía, a su vez, debe contar con credenciales específicas que deben ser registradas en el modelo de compañía correspondiente. La ausencia de estas credenciales impedirá el acceso a las APIs del sistema, ya que son necesarias para autenticar y autorizar las solicitudes.

Además, el sistema ha sido diseñado con un modelo que asigna roles específicos a los usuarios. Estos roles determinan el acceso a diversas vistas y funcionalidades dentro del sistema. Por lo tanto, es esencial que se configuren correctamente los roles para garantizar que los usuarios puedan acceder a las áreas pertinentes según sus permisos. Sin una configuración adecuada de credenciales y roles, el acceso a las funcionalidades del sistema puede ser restringido o denegado.
#
1. # <a name="_toc178152725"></a>**Frecuencia de ejecución de la solución**

El aplicativo se ejecuta en tiempo real de acuerdo con las condiciones del pseudocódigo
