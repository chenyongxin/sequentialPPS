!> Sequentially output binary scalar field data from mimic multiprocessors program.
!> @author CHEN Yongxin
program main

  implicit none

  character, parameter :: lf=char(10)
  integer,parameter :: pn(3) = [4,4,4]          ! partitions in 3D
  integer,parameter :: n(3)  = [8,4,4]          ! local grid number
  integer :: id, extent(6), wholeExtent(6)
  real :: a(n(1), n(2), n(3))
  integer :: pi, pj, pk, i, j, k, num

  ! global extent
  wholeExtent( ::2) = 1
  wholeExtent(2::2) = pn*n

  ! init file
  call init("data", pn, num)

  ! loop over partitions
  do pk = 1, pn(3)
     do pj = 1, pn(2)
        do pi = 1, pn(1)

           ! get id
           id = pi + (pj-1)*pn(1) + (pk-1)*pn(1)*pn(2)

           ! local extent
           extent(::2)  = ([pi,pj,pk]-1) * n + 1    ! starting indices, 1 is the fisrt entity
           extent(2::2) = extent(::2) + n - 1       ! ending indices

           ! construct local data
           forall(i=1:n(1),j=1:n(2),k=1:n(3)) a(i,j,k) = &
                ((pk-1)*n(3)+k-1)*pn(1)*n(1)*pn(2)*n(2) + &
                ((pj-1)*n(2)+j-1)*pn(1)*n(1) + (pi-1)*n(1)+i

           ! write partition data
           call write(num, id, extent, wholeExtent, a)

        end do
     end do
  end do

  ! finalize output
  call finalize(num)
contains

  !> Initialize a file and return file handle
  subroutine init(fname, pn, num)
    character(*), intent(in) :: fname
    integer, intent(in)  :: pn(3)
    integer, intent(out) :: num
    open(newunit=num, file=fname, form='unformatted', access='stream', status='replace')
    write(num) pn
  end subroutine init

  !> Write partition data
  subroutine write(num, id, extent, wholeExtent, a)
    integer, intent(in) :: num
    integer, intent(in) :: id
    integer, intent(in) :: extent(6)
    integer, intent(in) :: wholeExtent(6)
    real, intent(in)    :: a(:,:,:)
    write(num) id, extent, wholeExtent, 4*size(a), real(a, 4)
  end subroutine write

  !> Finalize a file
  subroutine finalize(num)
    integer, intent(in) :: num
    close(num)
  end subroutine finalize

end program main
