#!/bin/sh

export AWS_ACCESS_KEY=""
export AWS_SECRET_KEY=""

STAMP=`date +%d-%m-%Y.%H%M`
BUCKET='backups'
PREFIX='niwibe'
S3PUT='/usr/local/bin/s3put.py'
BACKUPPREFIX="/opt"
BACKUPDIR="www"

cd /tmp
tar cvJf $STAMP.tar.xz -C $BACKUPPREFIX $BACKUPDIR | exit
$S3PUT --prefix="$PREFIX" --bucket="$BUCKET" $STAMP.tar.xz | exit
rm $STAMP.tar.xz


