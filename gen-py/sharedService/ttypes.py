#
# Autogenerated by Thrift Compiler (0.9.3)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class Node:
  """
  Attributes:
   - name
   - data
   - creation
   - modification
   - version
   - children
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'name', None, None, ), # 1
    (2, TType.STRING, 'data', None, None, ), # 2
    (3, TType.STRING, 'creation', None, None, ), # 3
    (4, TType.STRING, 'modification', None, None, ), # 4
    (5, TType.I32, 'version', None, 0, ), # 5
    (6, TType.LIST, 'children', (TType.STRUCT,(Node, Node.thrift_spec)), None, ), # 6
  )

  def __init__(self, name=None, data=None, creation=None, modification=None, version=thrift_spec[5][4], children=None,):
    self.name = name
    self.data = data
    self.creation = creation
    self.modification = modification
    self.version = version
    self.children = children

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.name = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.data = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.creation = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.modification = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.I32:
          self.version = iprot.readI32()
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.LIST:
          self.children = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = Node()
            _elem5.read(iprot)
            self.children.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Node')
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 1)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.data is not None:
      oprot.writeFieldBegin('data', TType.STRING, 2)
      oprot.writeString(self.data)
      oprot.writeFieldEnd()
    if self.creation is not None:
      oprot.writeFieldBegin('creation', TType.STRING, 3)
      oprot.writeString(self.creation)
      oprot.writeFieldEnd()
    if self.modification is not None:
      oprot.writeFieldBegin('modification', TType.STRING, 4)
      oprot.writeString(self.modification)
      oprot.writeFieldEnd()
    if self.version is not None:
      oprot.writeFieldBegin('version', TType.I32, 5)
      oprot.writeI32(self.version)
      oprot.writeFieldEnd()
    if self.children is not None:
      oprot.writeFieldBegin('children', TType.LIST, 6)
      oprot.writeListBegin(TType.STRUCT, len(self.children))
      for iter6 in self.children:
        iter6.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.name)
    value = (value * 31) ^ hash(self.data)
    value = (value * 31) ^ hash(self.creation)
    value = (value * 31) ^ hash(self.modification)
    value = (value * 31) ^ hash(self.version)
    value = (value * 31) ^ hash(self.children)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
