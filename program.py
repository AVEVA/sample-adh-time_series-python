"""
This sample script demonstrates how to invoke the
Sequential Data Store REST API with Time Series data
"""


import json
import time
import jsonpatch
from adh_sample_library_preview import (SdsType, SdsTypeCode, SdsTypeProperty,
                                        EDSClient, ADHClient, SdsStream, Role)

SENDING_TO_ADH = True
TYPE_VALUE_TIME_NAME = "Value_Time"
TYPE_PRESSURE_TEMPERATURE_TIME_NAME = "Pressure_Temp_Time"

STREAM_PRESSURE_NAME = "Pressure_Tank1"
STREAM_TEMP_NAME = "Temperature_Tank1"
STREAM_TANK_0 = "Vessel"
STREAM_TANK_1 = "Tank1"
STREAM_TANK_2 = "Tank2"

VALUE_CACHE = []
VALUE_CACHE_2 = []



def get_appsettings():
    """Open and parse the appsettings.json file"""

    # Try to open the configuration file
    try:
        with open(
            'appsettings.json',
            'r',
        ) as f:
            appsettings = json.load(f)
    except Exception as error:
        print(f'Error: {str(error)}')
        print(f'Could not open/read appsettings.json')
        exit()

    return appsettings


def get_type_value_time():
    """Creates a type for value/time events"""

    double_type = SdsType("doubleType", SdsTypeCode.Double)
    time_type = SdsType("string", SdsTypeCode.DateTime)
    value = SdsTypeProperty("value", False, double_type)
    time_prop = SdsTypeProperty("time", True, time_type)

    type_value_time = SdsType(TYPE_VALUE_TIME_NAME, SdsTypeCode.Object, [value, time_prop],
                              description="A Time-Series indexed type with a value")

    return type_value_time


def get_type_press_temp_time():
    """Creates a type for press/temp/time events"""

    double_type = SdsType("doubleType", SdsTypeCode.Double)
    time_type = SdsType("string", SdsTypeCode.DateTime)
    temperature = SdsTypeProperty("temperature", False, double_type)
    pressure = SdsTypeProperty("pressure", False, double_type)
    time_prop = SdsTypeProperty("time", True, time_type)

    type_press_temp_time = SdsType(TYPE_PRESSURE_TEMPERATURE_TIME_NAME, SdsTypeCode.Object,
                                   [temperature, pressure, time_prop],
                                   description="A Time-Series indexed type with 2 values")

    return type_press_temp_time


def get_data():
    """Creates a set of data for use in the sample"""

    values = []
    values.append({"pressure": 346, "temperature": 91,
                   "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 0, "temperature": 0,
                   "time": "2017-01-11T22:22:23.430Z"})
    values.append({"pressure": 386, "temperature": 93,
                   "time": "2017-01-11T22:24:23.430Z"})
    values.append({"pressure": 385, "temperature": 92,
                   "time": "2017-01-11T22:25:23.430Z"})
    values.append({"pressure": 385, "temperature": 0,
                   "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92,
                   "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2,
                   "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 0,
                   "time": "2017-01-11T22:28:29.430Z"})
    return values


def get_data_tank_2():
    """Creates a set of data for use in the sample"""

    values = []
    values.append({"pressure": 345, "temperature": 89,
                   "time": "2017-01-11T22:20:23.430Z"})
    values.append({"pressure": 356, "temperature": 0,
                   "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 354, "temperature": 88,
                   "time": "2017-01-11T22:22:23.430Z"})
    values.append({"pressure": 374, "temperature": 87,
                   "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.5, "temperature": 88,
                   "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2,
                   "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 87,
                   "time": "2017-01-11T22:28:29.430Z"})

    return values


def get_pressure_data():
    """Gets a set of pressure data"""

    vals = get_data()
    values = []
    for val in vals:
        values.append({"value": val["pressure"], "time": val["time"]})
    return values


def get_temperature_data():
    """Gets a set of temperature data"""

    vals = get_data()
    values = []
    for val in vals:
        values.append({"value": val["temperature"], "time": val["time"]})
    return values


def suppress_error(sds_call):
    """Suppress an error thrown by SDS"""
    try:
        sds_call()
    except Exception as error:
        print(f"Encountered Error: {error}")


def main(test=False):
    """This function is the main body of the SDS Time Series sample script"""
    exception = None
    try:
        appsettings = get_appsettings()
        tenant_id = appsettings.get('TenantId')
        namespace_id = appsettings.get('NamespaceId')
        community_id = appsettings.get('CommunityId')

        # step 1
        if tenant_id == 'default' and namespace_id == 'default':
            sds_client = EDSClient(
                appsettings.get('ApiVersion'),
                appsettings.get('Resource'))
        else:
            sds_client = ADHClient(
                appsettings.get('ApiVersion'),
                appsettings.get('TenantId'),
                appsettings.get('Resource'),
                appsettings.get('ClientId'),
                appsettings.get('ClientSecret'),
                False)

        # step 2
        print('Creating value and time type')
        time_value_type = get_type_value_time()
        time_value_type = sds_client.Types.getOrCreateType(
            namespace_id, time_value_type)

        # step 3
        print('Creating a stream for pressure and temperature')
        pressure_stream = SdsStream(STREAM_PRESSURE_NAME, time_value_type.Id,
                                    description="A stream for pressure data of tank1")
        sds_client.Streams.createOrUpdateStream(namespace_id, pressure_stream)
        temperature_stream = SdsStream(STREAM_TEMP_NAME, time_value_type.Id,
                                       description="A stream for temperature data of tank1")
        sds_client.Streams.createOrUpdateStream(
            namespace_id, temperature_stream)

        # step 4
        sds_client.Streams.insertValues(namespace_id,
                                        pressure_stream.Id,
                                        json.dumps((get_pressure_data())))
        sds_client.Streams.insertValues(namespace_id,
                                        temperature_stream.Id,
                                        json.dumps((get_temperature_data())))

        # step 5
        print('Creating a tank type that has both stream and temperature')
        tank_type = get_type_press_temp_time()
        tank_type = sds_client.Types.getOrCreateType(namespace_id, tank_type)

        # step 6
        print('Creating a tank stream')
        tank_stream = SdsStream(STREAM_TANK_1, tank_type.Id,
                                description="A stream for data of tank1s")
        sds_client.Streams.createOrUpdateStream(namespace_id, tank_stream)

        # step 7
        sds_client.Streams.insertValues(namespace_id, STREAM_TANK_1,
                                        json.dumps(get_data()))

        print()
        print()
        print('Looking at the data in the system.  In this case we have some'
              'null values that are encoded as 0 for the value.')
        data = get_data()
        tank_1_sorted = sorted(data, key=lambda x: x['time'], reverse=False)
        print()
        print('Value we sent:')
        print(tank_1_sorted[1])
        first_time = tank_1_sorted[0]['time']
        last_time = tank_1_sorted[-1]['time']

        # step 8
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_PRESSURE_NAME, first_time, last_time)

        print()
        print('Value from pressure stream:')
        print((results)[1])

        print()
        print('Value from tank1 stream:')
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_TANK_1, first_time, last_time)
        print((results)[1])

        # step 9
        print()
        print()
        print("turning on verbosity")
        sds_client.acceptverbosity = True

        print("This means that will get default values back (in our case"
              " 0.0 since we are looking at doubles)")

        print()
        print('Value from pressure stream:')
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_PRESSURE_NAME, first_time, last_time)
        print((results)[1])
        print()
        print('Value from tank1 stream:')
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_TANK_1, first_time, last_time)
        print((results)[1])

        # step 10

        print()
        print()
        print("Getting data summary")
        # the count of 1 refers to the number of intervals requested
        summary_results = sds_client.Streams.getSummaries(
            namespace_id, STREAM_TANK_1, None, first_time, last_time, 1)
        print(summary_results)

        print()
        print()
        print('Now we want to look at data across multiple tanks.')
        print('For that we can take advantage of bulk stream calls')
        print('Creating new tank streams')
        tank_stream = SdsStream(STREAM_TANK_2, tank_type.Id,
                                description="A stream for data of tank2")
        sds_client.Streams.createOrUpdateStream(namespace_id, tank_stream)

        data_tank_2 = get_data_tank_2()
        sds_client.Streams.insertValues(
            namespace_id, STREAM_TANK_2, json.dumps(get_data_tank_2()))

        tank_2_sorted = sorted(
            data_tank_2, key=lambda x: x['time'], reverse=False)
        first_time_tank_2 = tank_2_sorted[0]['time']
        last_time_tank_2 = tank_2_sorted[-1]['time']

        tank_stream = SdsStream(STREAM_TANK_0, tank_type.Id, description="")
        sds_client.Streams.createOrUpdateStream(namespace_id, tank_stream)

        sds_client.Streams.insertValues(
            namespace_id, STREAM_TANK_0, json.dumps(get_data()))

        time.sleep(10)

        # step 11
        print('Getting bulk call results')
        results = sds_client.Streams.getStreamsWindow(
            namespace_id, [STREAM_TANK_0, STREAM_TANK_2], None,
            first_time_tank_2, last_time_tank_2)
        print(results)

        #######################################################################
        # Community steps
        #######################################################################
        if (community_id):
            # step 12
            print()
            print('Get tenant roles')
            roles = sds_client.Roles.getRoles()
            role: Role = None
            for r in roles:
                if r.RoleTypeId == sds_client.Roles.CommunityMemberRoleTypeId and r.CommunityId == community_id:
                    role = r
                    break
            print('Community member Id:')
            print(role.Id)

            print()
            print('Sharing stream to community')
            patch = jsonpatch.JsonPatch(
                [{
                    'op': 'add', 'path': '/RoleTrusteeAccessControlEntries/-',
                    'value': {
                        'AccessRights': 1, 'AccessType': 0,
                        'Trustee': {'ObjectId': role.Id, 'TenantId': None, 'Type': 'Role'}
                    }
                }])
            sds_client.Streams.patchAccessControl(
                namespace_id, STREAM_PRESSURE_NAME, patch)

            # step 13
            print()
            print('Searching the community')
            community_streams = sds_client.Communities.getCommunityStreams(
                community_id, STREAM_PRESSURE_NAME)
            print('Found matching streams:')
            for s in community_streams:
                print(s.Id)

            # step 14
            print()
            print('Getting stream data from the community stream')
            community_stream = community_streams[0]
            community_data = sds_client.Streams.getLastValueUrl(
                community_stream.Self)
            print('Retrieved last value:')
            print(community_data['value'])

    except Exception as ex:
        exception = ex
        print(f"Encountered Error: {ex}")
        print()

    finally:
        # step 15
        print()
        print()
        print()
        print("Cleaning up")
        print("Deleting the stream")
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_PRESSURE_NAME))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TEMP_NAME))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TANK_0))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TANK_1))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TANK_2))

        print("Deleting the types")
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, TYPE_PRESSURE_TEMPERATURE_TIME_NAME))
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, TYPE_VALUE_TIME_NAME))

        if test and exception is not None:
            raise exception
    print('Complete!')


if __name__ == '__main__':
    main()
