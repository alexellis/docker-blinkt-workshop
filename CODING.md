### Coding on the Pi

This document covers coding on the Pi.

There are three simple ways you can synchronize code between your laptop or the Pi.

### Edit on the device

Editing on the device is the simplest option if you are familiar with UNIX text-based editors.

* Nano

Beginners may use the pre-supplied `nano` editor to edit and create files.

Usage:

```
$ nano filename.py
```

|Command           | Description            |
-------------------|------------------------
| `Control + X`    | Exit                   |
| `Control + O`    | write file to the disk |
| `Control + K`    | cut a line             |
| `Control + U`    | paste a line           |
| `Control + W`    | find in current file   |

> For a nano cheat-sheet checkout: http://www.tuxradar.com/content/text-editing-nano-made-easy

* Cat

If you need to drop a single text file onto the Pi you can use the `cat` command and a bash pipe like this:

```
$ cat > Dockerfile
```

(Now paste the contents in)

```
FROM armhf/alpine:latest
CMD ["cat", "/etc/hostname"]
```

(Now it Control + D)

You'll see your file created in the current directory. I use this technique a lot when working on remote systems.

### Use `sftp/scp`

If you edit the code on your local computer then you can copy files up to the Raspberry Pi like this:

```
$ scp -r lab2_2 pi@raspberrypi.local:~/
```

That will copy the `lab2_2` folder from your laptop to the home directory on the Pi.

Copying from the Pi to the laptop is also useful:

```
$ scp -r pi@raspberrypi.local:~/lab2_2 .
```

### Use `git`

You can create a repository on Github and use `git push` and `git pull` to synchronize files.

[Getting started with Git](https://git-scm.com/book/en/v1/Getting-Started)

#### Advanced techniques

You can mount a NFS or Samba filesystem from the Pi to your laptop or visa-versa. This is an advanced technique and will take some time to setup.
