exec 5>&1
FF=$(echo aaa|tee >(cat - >&5))
echo $FF