"""-------------------------FUNCTIONS TO BE IMPORTED-------------------------"""


def get_link(cursor, hashed):
    """
    return link that corresponds hashed
    """
    sql = f"SELECT origin FROM links WHERE hash LIKE '%{hashed}%'"
    link = cursor.execute(sql).fetchone()
    if link is None:
        return link
    return link[0]


def add_link(cursor, link, domain):
    """
    update database with new link
    return hashed link
    """
    hashed = get_new_hash()
    hashedLink = f"{domain}{hashed}"
    if link is not None and "http" not in link:
        link = f"https://{link}"
    if is_new_link(cursor, link):
        add_hash(cursor, link, hashedLink)
    else:
        update_hash(cursor, link, hashedLink)
    return hashedLink


"""-----------------------------INTERNAL LOGIC-----------------------------"""


def get_new_hash():
    """
    return next hash
    """
    with open('lastHash.txt', 'r', encoding="utf-8") as fr:
        oldHash = fr.read().strip()
        if oldHash == '':
            oldHash = '/'   # symbol before '0' in ASCII
    newHash = iter_hash(oldHash, len(oldHash)-1)
    with open('lastHash.txt', 'w', encoding="utf-8") as fw:
        fw.write(newHash)
    return newHash


def iter_hash(hashed, index):
    """
    make "incrementing" of hashed
    """
    s = hashed[index]
    if s == '9':
        s = 'A'
    elif s == 'Z':
        s = 'a'
    elif s == 'z':
        if index == 0:    # increase len of hash
            return "0"*(len(hashed)+1)
        hashed = f"{hashed[:index]}{'0'}{hashed[index+1:]}"
        return iter_hash(hashed, index-1)
    else:
        s = chr(ord(s) + 1)
    return f"{hashed[:index]}{s}{hashed[index+1:]}"


def is_new_link(cursor, link):
    """
    checks whether link is new in database
    """
    sql = "SELECT * FROM links WHERE origin=?"
    duplicates = cursor.execute(sql, [link]).fetchall()
    return True if duplicates == [] else False


def add_hash(cursor, origin, hashed):
    """
    add row (link, hashed) to database (in case link is new)
    """
    cursor.execute(f"INSERT INTO links (origin, hash) VALUES (?, ?)", (origin, f"['{hashed}']"))


def update_hash(cursor, origin, new_hash):
    """
    update list of hashed in database (in case link is not new)
    """
    prevHash = get_hash_list(cursor, origin)
    newHashList = f"{str(prevHash)[0:-2]}', '{new_hash}']"
    sql = "UPDATE links SET hash=? WHERE origin=?"
    cursor.execute(sql, [newHashList, origin])


def get_hash_list(cursor, link):
    """
    get all hashes that corresponds link
    """
    sql = "SELECT hash FROM links WHERE origin=?"
    hashed = cursor.execute(sql, [link]).fetchone()
    return eval(hashed[0])


def print_database(cursor):
    cursor.execute('SELECT * FROM links')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], row[1])


def clear_database(cursor):
    sql = "DELETE FROM links"
    cursor.execute(sql)

