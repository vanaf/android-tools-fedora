#!/usr/bin/ruby

# Android build system is complicated and does not allow to build
# separate parts easily.
# This script tries to mimic Android build rules.

def expand(dir, files)
  files.map{|f| File.join(dir,f)}
end

# Compiles sources to *.o files.
# Returns array of output *.o filenames
def compile(sources, cflags)
  outputs = []
  for s in sources
    ext = File.extname(s)
    
    case ext
    when '.c'
        cc = 'gcc'
    	lang_flags = '-std=gnu11 $CFLAGS $CPPFLAGS'
    when '.cpp', '.cc'
        cc = 'g++'
    	lang_flags = '-std=gnu++14 $CXXFLAGS $CPPFLAGS'
    else
        raise "Unknown extension #{ext}"
    end

    output = s + '.o'
    outputs << output
    puts "#{cc} -o #{output} #{lang_flags} #{cflags} -c #{s}\n"
  end

  return outputs
end

# Links object files
def link(output, objects, ldflags)
  puts "g++ -o #{output} #{ldflags} $LDFLAGS #{objects.join(' ')}"
end

minicryptfiles = %w(
  dsa_sig.c
  p256_ec.c
  rsa.c
  sha.c
  p256.c
  p256_ecdsa.c
  sha256.c
)
libminicrypt = compile(expand('libmincrypt', minicryptfiles), '-Iinclude')

adbdfiles = %w(
  adb.cpp
  adb_auth.cpp
  adb_io.cpp
  adb_listeners.cpp
  adb_utils.cpp
  sockets.cpp
  transport.cpp
  transport_local.cpp
  transport_usb.cpp
  services.cpp
  adb_trace.cpp
  get_my_path_linux.cpp
  usb_linux.cpp
  diagnose_usb.cpp
  adb_auth_host.cpp
  sysdeps_unix.cpp
)
libadbd = compile(expand('adb', adbdfiles), '-DADB_REVISION=\"$PKGVER\" -DADB_HOST=1 -fpermissive -Iinclude -Ibase/include')

adbshfiles = %w(
  fdevent.cpp
  shell_service.cpp
  shell_service_protocol.cpp
)
libadbsh = compile(expand('adb', adbshfiles), '-DADB_REVISION=\"$PKGVER\" -DADB_HOST=0 -D_Nonnull= -D_Nullable= -fpermissive -Iadb -Iinclude -Ibase/include')

adbfiles = %w(
  console.cpp
  commandline.cpp
  adb_client.cpp
  file_sync_client.cpp
  line_printer.cpp
  client/main.cpp
)
libadb = compile(expand('adb', adbfiles), '-DADB_REVISION=\"$PKGVER\" -D_GNU_SOURCE -DADB_HOST=1 -D_Nonnull= -D_Nullable= -fpermissive -Iadb -Iinclude -Ibase/include')

basefiles = %w(
  file.cpp
  logging.cpp
  parsenetaddress.cpp
  stringprintf.cpp
  strings.cpp
  errors_unix.cpp
)
libbase = compile(expand('base', basefiles), '-DADB_HOST=1 -D_GNU_SOURCE -Ibase/include -Iinclude')

logfiles = %w(
  logd_write.c
  log_event_list.c
  log_event_write.c
  fake_log_device.c
)
liblog = compile(expand('liblog', logfiles), '-DLIBLOG_LOG_TAG=1005 -DFAKE_LOG_DEVICE=1 -D_GNU_SOURCE -Ilog/include -Iinclude')

cutilsfiles = %w(
  load_file.c
  socket_inaddr_any_server_unix.c
  socket_local_client_unix.c
  socket_local_server_unix.c
  socket_loopback_client_unix.c
  socket_loopback_server_unix.c
  socket_network_client_unix.c
  threads.c
  sockets.cpp
  sockets_unix.cpp
)
libcutils = compile(expand('libcutils', cutilsfiles), '-D_GNU_SOURCE -Iinclude')

link('adb/adb', libbase + liblog + libcutils + libadbd + libadbsh + libadb, '-lrt -ldl -lpthread -lcrypto -lutil')


fastbootfiles = %w(
  socket.cpp
  tcp.cpp
  udp.cpp
  protocol.cpp
  engine.cpp
  bootimg_utils.cpp
  fastboot.cpp
  util.cpp
  fs.cpp
  usb_linux.cpp
  util_linux.cpp
)
libfastboot = compile(expand('fastboot', fastbootfiles), '-DFASTBOOT_REVISION=\"$PKGVER\" -D_GNU_SOURCE -Iadb -Iinclude -Imkbootimg -Ibase/include -Ilibsparse/include -I../extras/ext4_utils -I../extras/f2fs_utils')

sparsefiles = %w(
  backed_block.c
  output_file.c
  sparse.c
  sparse_crc32.c
  sparse_err.c
  sparse_read.c
)
libsparse = compile(expand('libsparse', sparsefiles), '-Ilibsparse/include')

zipfiles = %w(
  zip_archive.cc
)
libzip = compile(expand('libziparchive', zipfiles), '-Ibase/include -Iinclude')

utilfiles = %w(
  FileMap.cpp
)
libutil = compile(expand('libutils', utilfiles), '-Iinclude')

ext4files = %w(
  make_ext4fs.c
  ext4fixup.c
  ext4_utils.c
  allocate.c
  contents.c
  extent.c
  indirect.c
  sha1.c
  wipe.c
  crc16.c
  ext4_sb.c
)
libext4 = compile(expand('../extras/ext4_utils', ext4files), '-Ilibsparse/include -Iinclude')

link('fastboot/fastboot', libsparse + libzip + liblog + libutil + libcutils + libbase + libext4 + libfastboot + libadbsh + libadbd, '-lpthread -lselinux -lz -lcrypto -lutil')

