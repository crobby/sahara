.. _diskimage-builder-label:

Building Images for Vanilla Plugin
==================================

In this document you will find instruction on how to build Ubuntu, Fedora, and
CentOS images with Apache Hadoop versions 1.x.x and 2.x.x.

As of now the vanilla plugin works with images with pre-installed versions of
Apache Hadoop. To simplify the task of building such images we use
`Disk Image Builder <https://github.com/openstack/diskimage-builder>`_.

`Disk Image Builder` builds disk images using elements. An element is a
particular set of code that alters how the image is built, or runs within the
chroot to prepare the image.

Elements for building vanilla images are stored in
`Sahara extra repository <https://github.com/openstack/sahara-image-elements>`_

.. note::

   Sahara requires images with cloud-init package installed:

   * `For Fedora <http://pkgs.fedoraproject.org/cgit/cloud-init.git/>`_
   * `For Ubuntu <http://packages.ubuntu.com/precise/cloud-init>`_

To create vanilla images follow these steps:

1. Clone repository "https://github.com/openstack/sahara-image-elements" locally.

2. Use tox to build images.

   You can run "tox -e venv -- sahara-image-create" command in sahara-image-elements
   directory to build images. By default this script will attempt to create cloud
   images for all versions of supported plugins and all operating systems
   (subset of Ubuntu, Fedora, and CentOS depending on plugin). This command
   must be run with root privileges.

   .. sourcecode:: console

      tox -e venv -- sahara-image-create

   Tox will create a virtualenv and install required python packages in it,
   clone the repositories "https://github.com/openstack/diskimage-builder" and "https://github.com/openstack/sahara-image-elements" and export necessary parameters.
        * ``DIB_HADOOP_VERSION`` - version of Hadoop to install
        * ``JAVA_DOWNLOAD_URL`` - download link for JDK (tarball or bin)
        * ``OOZIE_DOWNLOAD_URL`` - download link for OOZIE (we have built
          Oozie libs here: http://sahara-files.mirantis.com/oozie-4.0.0.tar.gz)
        * ``HIVE_VERSION`` - version of Hive to install (currently supports only 0.11.0)
        * ``ubuntu_image_name``
        * ``fedora_image_name``
        * ``DIB_IMAGE_SIZE`` - parameter that specifies a volume of hard disk of
          instance. You need to specify it only for Fedora because Fedora doesn't use all available volume
        * ``DIB_COMMIT_ID`` - latest commit id of diskimage-builder project
        * ``SAHARA_ELEMENTS_COMMIT_ID`` - latest commit id of sahara-image-elements project

   NOTE: If you don't want to use default values, you should set your values of parameters.

   Then it will create required cloud images using image elements that install
   all the necessary packages and configure them. You will find created images in
   the parent directory.

.. note::

    Disk Image Builder will generate QCOW2 images, used with the default
    OpenStack Qemu/KVM hypervisors. If your OpenStack uses a different
    hypervisor, the generated image should be converted to an appropriate format.

    VMware Nova backend requires VMDK image format. You may use qemu-img
    utility to convert a QCOW2 image to VMDK.

    .. sourcecode:: console

        qemu-img convert -O vmdk <original_image>.qcow2 <converted_image>.vmdk


For finer control of diskimage-create.sh see the `official documentation
<https://github.com/openstack/sahara-image-elements/blob/master/diskimage-create/README.rst>`_
