import os, shutil, tempfile, bz2

def unbzip( filename, dest=None ):
    """Uncompress bzip files
    Parameters
    ----------
    filename : str
        Filename to load data from.
    """
    newfile = filename.rsplit('.', 1)[0]
    # If the results will be moved to other destination
    if dest:
        newfile = os.path.join(dest, os.path.basename(newfile))

    with open(newfile, 'wb') as new_file, bz2.BZ2File(filename, 'rb') as file:
        for data in iter(lambda : file.read(100 * 1024), b''):
            new_file.write(data)

def tmp_zip( data_in, prefix='xnat_' ):
    """Function to create a temporary zip file
    Parameters
    ----------
    data_in : str | list
        Folder if is a string or Files if a list
    """
    tmpdir = tempfile.mkdtemp()
    try:
        files = os.listdir(data_in) if isinstance( data_in, str ) else data_in
        # Moving all files to temporary directory
        for subfile in files:
            # When data_in is a folder, it completes the path
            if isinstance( data_in, str ):
                subfile = os.path.join(data_in, subfile)
            # Uncompressing bz files
            # TODO: Uncompress gz and zip
            if subfile.endswith('.bz'):
                unbzip(subfile, tmpdir)
            else:
                shutil.copy2(subfile, tmpdir)

        # Creating temporary zip name
        fzip = tempfile.NamedTemporaryFile(prefix=prefix)
        fzip.close()

        shutil.make_archive(fzip.name, 'zip', tmpdir)
    finally:
        shutil.rmtree(tmpdir)
    
    return fzip.name + '.zip'