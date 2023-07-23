#include <Python.h>

double ColourDistance(int e1[3], int e2[3])
{
    long rmean = ((long)e1[0] + (long)e2[0]) / 2;
    long r = (long)e1[0] - (long)e2[0];
    long g = (long)e1[1] - (long)e2[1];
    long b = (long)e1[2] - (long)e2[2];
    return sqrt((((512 + rmean) * r * r) >> 8) + 4 * g * g + (((767 - rmean) * b * b) >> 8));
}

int ShortestIndex(int pixel[3], int *colors, int len)
{
    int i, j;
    double shortest = 10000000;
    int shortestIndex;
    double dist;
    int color[3];
    for (i = 0; i < len; ++i)
    {
        for (j = 0; j < 3; ++j)
            color[j] = colors[i * 3 + j];
        dist = ColourDistance(pixel, color);
        if (dist < shortest)
        {
            shortest = dist;
            shortestIndex = i;
        }
    }
    return shortestIndex;
}

static PyObject *_color_distance(PyObject *self, PyObject *args)
{
    PyObject *color1;
    PyObject *color2;

    int *dbar1;
    int color1len;
    int *dbar2;
    int color2len;

    double result;
    int i;

    if (!PyArg_ParseTuple(args, "OO", &color1, &color2))
        return 0;

    ////////////// 1 //////////////
    color1 = PySequence_Fast(color1, "argument must be iterable");
    if (!color1)
        return 0;

    color1len = PySequence_Fast_GET_SIZE(color1);

    dbar1 = malloc(color1len * sizeof(int));
    if (!dbar1)
    {
        Py_DECREF(color1);
        return PyErr_NoMemory();
    }
    for (i = 0; i < color1len; i++)
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(color1, i);
        if (!item)
        {
            Py_DECREF(color1);
            free(dbar1);
            return 0;
        }
        fitem = PyNumber_Long(item);
        if (!fitem)
        {
            Py_DECREF(color1);
            free(dbar1);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return 0;
        }
        dbar1[i] = PyLong_AsLong(fitem);
        Py_DECREF(fitem);
    }

    /* clean up, compute, and return result */
    Py_DECREF(color1);

    ////////////// 2 //////////////
    color2 = PySequence_Fast(color2, "argument must be iterable");
    if (!color2)
        return 0;

    color2len = PySequence_Fast_GET_SIZE(color2);

    dbar2 = malloc(color2len * sizeof(int));
    if (!dbar2)
    {
        Py_DECREF(color2);
        return PyErr_NoMemory();
    }
    for (i = 0; i < color2len; i++)
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(color2, i);
        if (!item)
        {
            Py_DECREF(color2);
            free(dbar2);
            return 0;
        }
        fitem = PyNumber_Long(item);
        if (!fitem)
        {
            Py_DECREF(color2);
            free(dbar2);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return 0;
        }
        dbar2[i] = PyLong_AsLong(fitem);
        Py_DECREF(fitem);
    }

    /* clean up, compute, and return result */
    Py_DECREF(color2);

    ////////////// calc //////////////

    result = ColourDistance(dbar1, dbar2);
    free(dbar1);
    free(dbar2);
    return Py_BuildValue("d", result);
}

static PyObject *_shortest_index(PyObject *self, PyObject *args)
{
    PyObject *pixel;
    PyObject *colors;

    int *ipixel;
    int *icolors;
    int colorslen;

    int result;
    int i, j;

    if (!PyArg_ParseTuple(args, "OO", &pixel, &colors))
        return 0;

    ////////////// pixel //////////////
    pixel = PySequence_Fast(pixel, "argument must be iterable");
    if (!pixel)
        return 0;

    ipixel = malloc(3 * sizeof(int));
    if (!ipixel)
    {
        Py_DECREF(pixel);
        return PyErr_NoMemory();
    }

    for (i = 0; i < 3; i++)
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(pixel, i);
        if (!item)
        {
            Py_DECREF(pixel);
            free(ipixel);
            return 0;
        }
        fitem = PyNumber_Long(item);
        if (!fitem)
        {
            Py_DECREF(pixel);
            free(ipixel);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return 0;
        }
        ipixel[i] = PyLong_AsLong(fitem);
        Py_DECREF(fitem);
    }
    Py_DECREF(pixel);

    ////////////// colors //////////////
    colors = PySequence_Fast(colors, "argument must be iterable");
    if (!colors)
        return 0;

    colorslen = PySequence_Fast_GET_SIZE(colors);

    icolors = malloc((colorslen * 3) * sizeof(int));
    if (!icolors)
    {
        Py_DECREF(colors);
        return PyErr_NoMemory();
    }
    for (i = 0; i < colorslen; i++)
    {
        PyObject *item = PySequence_Fast_GET_ITEM(colors, i);
        if (!item)
        {
            Py_DECREF(colors);
            free(icolors);
            return 0;
        }
        for (j = 0; j < 3; j++)
        {
            PyObject *fitem;
            PyObject *value = PySequence_Fast_GET_ITEM(item, j);
            if (!value)
            {
                Py_DECREF(colors);
                free(icolors);
                return 0;
            }
            fitem = PyNumber_Long(value);
            if (!fitem)
            {
                Py_DECREF(colors);
                free(icolors);
                PyErr_SetString(PyExc_TypeError, "all items must be numbers");
                return 0;
            }
            icolors[i * 3 + j] = PyLong_AsLong(fitem);
            Py_DECREF(fitem);
        }
    }
    Py_DECREF(colors);

    result = ShortestIndex(ipixel, icolors, colorslen);
    free(ipixel);
    free(icolors);
    return Py_BuildValue("i", result);
}

static PyObject *version(PyObject *self)
{
    return Py_BuildValue("s", "version 1.0");
}

static PyMethodDef myMethods[] = {
    {"_color_distance", _color_distance, METH_VARARGS, "Calculate color distance"},
    {"_shortest_index", _shortest_index, METH_VARARGS, "Calculate shortest color distance index"},
    {"version", (PyCFunction)version, METH_NOARGS, "returns the version."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Color calculation module.",
    -1,
    myMethods};

PyMODINIT_FUNC PyInit_myModule(void)
{
    return PyModule_Create(&myModule);
}