#include <Python.h>

double Distance(int A[2], int B[2])
{
    long x = (long)A[0] - (long)B[0];
    long y = (long)A[1] - (long)B[1];
    return sqrt((x * x) + (y * y));
}

int ShortestIndex(int new_coord[2], int *coords, int len)
{
    int i, j;
    double shortest = 10000000;
    int shortestIndex;
    double dist;
    int coord[2];
    for (i = 0; i < len; ++i)
    {
        for (j = 0; j < 2; ++j)
            coord[j] = coords[i * 2 + j];
        dist = Distance(new_coord, coord);
        if (dist < shortest)
        {
            shortest = dist;
            shortestIndex = i;
        }
    }
    return shortestIndex;
}

int NeighbourIndex(int new_coord[2], int *coords, int len)
{
    int offsets[8][2] = {
        {0, 1},
        {1, 0},
        {0, -1},
        {-1, 0},
        {1, 1},
        {1, -1},
        {-1, 1},
        {-1, -1},

        {-2, -2},
        {-2, -1},
        {-2, 0},
        {-2, 1},
        {-2, 2},
        {-1, -2},
        {-1, 2},
        {0, -2},
        {0, 2},
        {1, -2},
        {1, 2},
        {2, -2},
        {2, -1},
        {2, 0},
        {2, 1},
        {2, 2},

        {-3, -3},
        {-3, -2},
        {-3, -1},
        {-3, 0},
        {-3, 1},
        {-3, 2},
        {-3, 3},
        {-2, -3},
        {-2, 3},
        {-1, -3},
        {-1, 3},
        {0, -3},
        {0, 3},
        {1, -3},
        {1, 3},
        {2, -3},
        {2, 3},
        {3, -3},
        {3, -2},
        {3, -1},
        {3, 0},
        {3, 1},
        {3, 2},
        {3, 3},
    };
    int i, j, k;
    int coord[2];
    int offset[2];
    int new_offsetted[2];
    for (k = 0; k < 8; ++k)
    {
        for (j = 0; j < 2; ++j)
            new_offsetted[j] = new_coord[j] + offsets[k][j];
        for (i = 0; i < len; ++i)
        {
            for (j = 0; j < 2; ++j)
                coord[j] = coords[i * 2 + j];
            if (new_offsetted[0] == coord[0] && new_offsetted[1] == coord[1])
                return i;
        }
    }
    return -1;
}

static PyObject *_shortest_index(PyObject *self, PyObject *args)
{
    PyObject *new_coord;
    PyObject *coords;

    int *inew_coord;
    int *icoords;
    int coordslen;

    int result;
    int i, j;

    if (!PyArg_ParseTuple(args, "OO", &new_coord, &coords))
        return 0;

    ////////////// new_coord //////////////
    new_coord = PySequence_Fast(new_coord, "argument must be iterable");
    if (!new_coord)
        return 0;

    inew_coord = malloc(2 * sizeof(int));
    if (!inew_coord)
    {
        Py_DECREF(new_coord);
        return PyErr_NoMemory();
    }

    for (i = 0; i < 2; i++)
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(new_coord, i);
        if (!item)
        {
            Py_DECREF(new_coord);
            free(inew_coord);
            return 0;
        }
        fitem = PyNumber_Long(item);
        if (!fitem)
        {
            Py_DECREF(new_coord);
            free(inew_coord);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return 0;
        }
        inew_coord[i] = PyLong_AsLong(fitem);
        Py_DECREF(fitem);
    }
    Py_DECREF(new_coord);

    ////////////// coords //////////////
    coords = PySequence_Fast(coords, "argument must be iterable");
    if (!coords)
        return 0;

    coordslen = PySequence_Fast_GET_SIZE(coords);

    icoords = malloc((coordslen * 2) * sizeof(int));
    if (!icoords)
    {
        Py_DECREF(coords);
        return PyErr_NoMemory();
    }
    for (i = 0; i < coordslen; i++)
    {
        PyObject *item = PySequence_Fast_GET_ITEM(coords, i);
        if (!item)
        {
            Py_DECREF(coords);
            free(icoords);
            return 0;
        }
        for (j = 0; j < 2; j++)
        {
            PyObject *fitem;
            PyObject *value = PySequence_Fast_GET_ITEM(item, j);
            if (!value)
            {
                Py_DECREF(coords);
                free(icoords);
                return 0;
            }
            fitem = PyNumber_Long(value);
            if (!fitem)
            {
                Py_DECREF(coords);
                free(icoords);
                PyErr_SetString(PyExc_TypeError, "all items must be numbers");
                return 0;
            }
            icoords[i * 2 + j] = PyLong_AsLong(fitem);
            Py_DECREF(fitem);
        }
    }
    Py_DECREF(coords);

    result = ShortestIndex(inew_coord, icoords, coordslen);
    free(inew_coord);
    free(icoords);
    return Py_BuildValue("i", result);
}

static PyObject *_neighbour_index(PyObject *self, PyObject *args)
{
    PyObject *new_coord;
    PyObject *coords;

    int *inew_coord;
    int *icoords;
    int coordslen;

    int result;
    int i, j;

    if (!PyArg_ParseTuple(args, "OO", &new_coord, &coords))
        return 0;

    ////////////// new_coord //////////////
    new_coord = PySequence_Fast(new_coord, "argument must be iterable");
    if (!new_coord)
        return 0;

    inew_coord = malloc(2 * sizeof(int));
    if (!inew_coord)
    {
        Py_DECREF(new_coord);
        return PyErr_NoMemory();
    }

    for (i = 0; i < 2; i++)
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(new_coord, i);
        if (!item)
        {
            Py_DECREF(new_coord);
            free(inew_coord);
            return 0;
        }
        fitem = PyNumber_Long(item);
        if (!fitem)
        {
            Py_DECREF(new_coord);
            free(inew_coord);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return 0;
        }
        inew_coord[i] = PyLong_AsLong(fitem);
        Py_DECREF(fitem);
    }
    Py_DECREF(new_coord);

    ////////////// coords //////////////
    coords = PySequence_Fast(coords, "argument must be iterable");
    if (!coords)
        return 0;

    coordslen = PySequence_Fast_GET_SIZE(coords);

    icoords = malloc((coordslen * 2) * sizeof(int));
    if (!icoords)
    {
        Py_DECREF(coords);
        return PyErr_NoMemory();
    }
    for (i = 0; i < coordslen; i++)
    {
        PyObject *item = PySequence_Fast_GET_ITEM(coords, i);
        if (!item)
        {
            Py_DECREF(coords);
            free(icoords);
            return 0;
        }
        for (j = 0; j < 2; j++)
        {
            PyObject *fitem;
            PyObject *value = PySequence_Fast_GET_ITEM(item, j);
            if (!value)
            {
                Py_DECREF(coords);
                free(icoords);
                return 0;
            }
            fitem = PyNumber_Long(value);
            if (!fitem)
            {
                Py_DECREF(coords);
                free(icoords);
                PyErr_SetString(PyExc_TypeError, "all items must be numbers");
                return 0;
            }
            icoords[i * 2 + j] = PyLong_AsLong(fitem);
            Py_DECREF(fitem);
        }
    }
    Py_DECREF(coords);

    result = NeighbourIndex(inew_coord, icoords, coordslen);
    free(inew_coord);
    free(icoords);
    return Py_BuildValue("i", result);
}

static PyObject *version(PyObject *self)
{
    return Py_BuildValue("s", "version 1.0");
}

static PyMethodDef myMethods[] = {
    {"_shortest_index", _shortest_index, METH_VARARGS, "Calculate shortest distance index"},
    {"_neighbour_index", _neighbour_index, METH_VARARGS, "Calculate neighbouring pixel index"},
    {"version", (PyCFunction)version, METH_NOARGS, "returns the version."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Distance calculation module.",
    -1,
    myMethods};

PyMODINIT_FUNC PyInit_myModule(void)
{
    return PyModule_Create(&myModule);
}